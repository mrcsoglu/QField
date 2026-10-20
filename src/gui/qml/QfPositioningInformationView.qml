import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.qgis
import org.qfield.core
import org.qfield.gui

/**
 * Compact field-friendly positioning information view.
 *
 * Keeps the QfPositioningInformationModel and public aliases intact so the
 * existing QfInformationDrawer can host this component without changes.
 */
Rectangle {
  id: positioningInformationView

  property alias positionSource: positioningInformationModel.positioningSource
  property alias antennaHeight: positioningInformationModel.antennaHeight

  // Preserved compatibility properties for existing QML consumers.
  property color backgroundColor: "transparent"
  property color alternateBackgroundColor: QfTheme.positionBackgroundColor
  property color textColor: hasPosition ? QfTheme.mainTextColor : QfTheme.secondaryTextColor
  property double cellHeight: 26
  property double cellPadding: 6
  property real contentHeight: contentLayout.implicitHeight + 24

  readonly property var gpsInfo: positionSource ? positionSource.positionInformation : null
  readonly property bool hasPosition: gpsInfo !== null && gpsInfo.latitudeValid && gpsInfo.longitudeValid
  readonly property real latitude: hasPosition ? Number(gpsInfo.latitude) : NaN
  readonly property real longitude: hasPosition ? Number(gpsInfo.longitude) : NaN
  readonly property bool supportsUtm: hasPosition && latitude >= -80 && latitude <= 84
  readonly property int utmZone: supportsUtm ? Math.max(1, Math.min(60, Math.floor((longitude + 180) / 6) + 1)) : 0
  readonly property string utmBand: {
    if (!supportsUtm) return "";
    const letters = "CDEFGHJKLMNPQRSTUVWX";
    return letters.charAt(Math.max(0, Math.min(19, Math.floor((latitude + 80) / 8))));
  }
  readonly property string utmPrefix: supportsUtm ? utmZone + utmBand : ""

  function copyLocation() {
    if (!hasPosition) return;
    try {
      const p = QfGeometryUtils.reprojectPoint(
        QfGeometryUtils.point(longitude, latitude),
        QfCoordinateReferenceSystemUtils.wgs84Crs(),
        positioningInformationModel.coordinateDisplayCrs);
      const x = Number(p.x);
      const y = Number(p.y);
      if (!isFinite(x) || !isFinite(y)) return;
      const text = (supportsUtm ? utmPrefix + " " : "") +
                   Math.round(x) + " " + Math.round(y);
      platformUtilities.copyTextToClipboard(text);
      iface.mainWindow().displayToast(qsTr("Koordinat kopyalandı"));
    } catch (e) {
      console.warn("Position card could not copy coordinate: " + e);
    }
  }

  color: QfTheme.mainBackgroundColorSemiOpaque
  width: parent ? parent.width : 320
  clip: true

  QfPositioningInformationModel {
    id: positioningInformationModel
    distanceUnits: projectInfo.distanceUnits
    // Automatically display WGS84 UTM in the correct zone, where supported.
    // Outside UTM bounds, respect QField's normal display CRS.
    coordinateDisplayCrs: positioningInformationView.supportsUtm
      ? QfCoordinateReferenceSystemUtils.fromDescription(
          "EPSG:" + ((positioningInformationView.latitude >= 0 ? 32600 : 32700) +
                     positioningInformationView.utmZone))
      : projectInfo.coordinateDisplayCrs
  }

  ColumnLayout {
    id: contentLayout
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.margins: 12
    spacing: 8

    RowLayout {
      Layout.fillWidth: true
      spacing: 8

      ColumnLayout {
        Layout.fillWidth: true
        spacing: 1

        Text {
          text: qsTr("Konumum")
          color: QfTheme.mainTextColor
          font.bold: true
          font.pixelSize: 15
        }
        Text {
          text: positioningInformationView.supportsUtm
            ? qsTr("WGS84 / UTM ") + positioningInformationView.utmPrefix
            : qsTr("Konum bekleniyor")
          color: QfTheme.secondaryTextColor
          font: QfTheme.tipFont
        }
      }

      QfButton {
        text: qsTr("Kopyala")
        enabled: positioningInformationView.hasPosition
        onClicked: positioningInformationView.copyLocation()
      }
    }

    Flow {
      id: infoCards
      Layout.fillWidth: true
      Layout.preferredHeight: childrenRect.height
      spacing: 8

      Repeater {
        model: positioningInformationModel

        Rectangle {
          readonly property bool isCoordinate: index < 2
          readonly property bool hasUsefulValue: Value !== undefined && Value !== null &&
                                                  String(Value).length > 0 &&
                                                  String(Value) !== "N/A" &&
                                                  String(Value) !== "Yok"
          visible: index < 6 && (isCoordinate || hasUsefulValue)
          width: isCoordinate
            ? Math.max(120, (infoCards.width - infoCards.spacing) / 2)
            : Math.max(100, (infoCards.width - infoCards.spacing * 2) / 3)
          height: isCoordinate ? 64 : 46
          radius: 9
          color: QfTheme.groupBoxBackgroundColor

          Column {
            anchors.fill: parent
            anchors.margins: 9
            spacing: 4

            Text {
              width: parent.width
              text: index === 0 ? qsTr("Doğu (X)") :
                    index === 1 ? qsTr("Kuzey (Y)") : Name
              color: QfTheme.secondaryTextColor
              font: QfTheme.tipFont
              elide: Text.ElideRight
            }

            Text {
              width: parent.width
              text: Value ? String(Value) : "—"
              color: positioningInformationView.textColor
              font.pixelSize: isCoordinate ? 17 : 13
              font.bold: isCoordinate
              elide: Text.ElideRight
            }
          }
        }
      }
    }
  }
}
