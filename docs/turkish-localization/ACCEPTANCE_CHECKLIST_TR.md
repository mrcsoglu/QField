# Platform kabul kontrol listesi

Otomatik katalog ve Qt çalışma zamanı testleri Windows üzerinde yürütülmüştür.
Bir platformda gerçek QField uygulaması veya fiziksel aygıt kullanılmadıysa sonuç
**Test edilmedi** olarak bırakılmıştır.

| Kontrol | Windows | Android | iOS |
|---|---|---|---|
| TS yapısı, yer tutucular, HTML ve numerus | Geçti | Aynı derlenmiş katalog | Aynı derlenmiş katalog |
| Qt 6 `lrelease` ile QM derleme | Geçti | Aynı QM pakette | Aynı QM pakette |
| Qt `QTranslator` çalışma zamanı aramaları | Geçti | Test edilmedi | Test edilmedi |
| `qmllint` ile eklenti `main.qml` denetimi | Geçti | Aynı QML pakette | Aynı QML pakette |
| ZIP kökü ve zorunlu eklenti dosyaları | Geçti | Aynı ZIP pakette | Aynı ZIP pakette |
| QField'e ZIP kurma ve eklentiyi etkinleştirme | Test edilmedi | Test edilmedi | Test edilmedi |
| Ana ekran, proje seçimi ve ayarlar | Test edilmedi | Test edilmedi | Test edilmedi |
| Harita, katman, lejant ve görünürlük | Test edilmedi | Test edilmedi | Test edilmedi |
| Nesne sorgulama ve öznitelik formu | Test edilmedi | Test edilmedi | Test edilmedi |
| Nokta/çizgi/poligon ekleme ve düzenleme | Test edilmedi | Test edilmedi | Test edilmedi |
| Processing algoritması adı, parametresi ve yardımı | Test edilmedi | Test edilmedi | Test edilmedi |
| Koordinat, KRS, ölçme ve yakalama | Test edilmedi | Test edilmedi | Test edilmedi |
| GNSS, NTRIP ve konum doğruluğu | Test edilmedi | Test edilmedi | Test edilmedi |
| Arama, filtre ve yer imleri | Test edilmedi | Test edilmedi | Test edilmedi |
| Fotoğraf, dosya ve ekler | Test edilmedi | Test edilmedi | Test edilmedi |
| QFieldCloud giriş ve eşitleme | Test edilmedi | Test edilmedi | Test edilmedi |
| Uzun metinlerde kesilme veya taşma | Test edilmedi | Test edilmedi | Test edilmedi |
| Performans gerilemesi | Test edilmedi | Test edilmedi | Test edilmedi |
| Eklentiyi kaldırma ve yeniden başlatma | Test edilmedi | Test edilmedi | Test edilmedi |

“Aynı derlenmiş katalog/paket” yalnızca platformlara dağıtılan dosyanın aynı
olduğunu belirtir; gerçek cihaz testinin yerini tutmaz.

