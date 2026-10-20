# Çeviri envanteri ve kalite raporu

## Sabitlenen kaynaklar

- QField `v4.3.6`: `d093eeba97c1a791b93ab1d059c91c7c57ec79cf`
- QField'in vcpkg portunda sabitlediği QGIS:
  `3a92eb30c83d7d52751a330628d72b8eb9e64876`

Qt 6 `lupdate -locations none -recursive src` ile QField kaynak ağacı yeniden
taranmıştır. QGIS tarafında `src/analysis/processing` ve
`src/core/processing` bütünü 3.885 ileti üretmiştir. QField'in kaynak kodunda
uygulanan `SupportsInPlaceEdits` filtresine karşılık gelen 87 algoritma kaynak
dosyasının statik envanteri 726 iletidir.

| Katalog | Etkin kaynak | Tamamlanmış | Eksik/boş | Unfinished |
|---|---:|---:|---:|---:|
| QField arayüzü | 1.445 | 1.445 | 0 | 0 |
| QGIS Native Processing çalışma kümesi | 726 | 726 | 0 | 0 |
| Birleşik eklenti kataloğu | 2.169 | 2.169 | 0 | 0 |

Birleşik sayının 2.171 yerine 2.169 olmasının nedeni `QObject` bağlamındaki
`Distance` ve `Point` iletilerinin iki kaynakta da aynı anahtarla bulunmasıdır.
Birleştirme anahtarı `(context, source, comment, numerus)` biçimindedir.

## Dil kalite yaklaşımı

Kataloglar çevrimiçi veya çalışma anında makine çeviri hizmetine gönderilmez.
QField bağlamları ve QGIS algoritma kaynakları incelenerek elle hazırlanmış,
tekrarlanabilir düzeltme sözlükleri uygulanır. Yalnızca İngilizce kalan metinler
değil; eski Türkçe katalogdaki `obje`, `özellik`, `vertex`, `grid`, parantezli
çoğul ekleri ve kullanıcıya anlam aktarmayan sözcüğü sözcüğüne çeviriler de
yeniden yazılmıştır.

Başlıca kararlar: `feature` → `nesne`, `field` → `alan`, `buffer` → `tampon
bölge`, `dissolve` → `ortak sınırları kaldırarak birleştir`, geometri işlemi
`translate` → `ötele`, `snapping` → `yakalama`, `map canvas` → `harita tuvali`,
`latitude/longitude` → `enlem/boylam`, `easting/northing` → `doğu/kuzey
koordinatı`, ağ terimi `port` → `port`.

## Bilinçli olarak çevrilmeyenler

Ürün ve standart adları, protokoller, şema anahtarları ve birim kısaltmaları
anlam bozulmasını önlemek için korunur: QField, QFieldCloud, QGIS, GNSS, NTRIP,
EPSG, WGS84, UTM, GPS, PDOP, HDOP, VDOP, RTK, DGPS, IMU, TCP, UDP, SSL/TLS,
NULL, KB/MB/GB/TB/B ve benzerleri. `Oval` ve `Normal` Türkçede de aynı yazılır.

Katalog denetimi Qt yer tutucularını, HTML işaretlemesini, satır sonlarını,
çoğul yapılarını, boş/unfinished iletileri ve aynı kaynak için tutarsız karşılıkları
denetler. Gerçek cihazda metin taşması ve kullanıcı deneyimi ayrıca sınanmalıdır.

