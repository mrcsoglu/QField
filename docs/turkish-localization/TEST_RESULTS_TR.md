# Test sonuçları

Hedef QField: `v4.3.6` (`d093eeba97c1a791b93ab1d059c91c7c57ec79cf`).
Hedef QGIS: `3a92eb30c83d7d52751a330628d72b8eb9e64876`.

| Kontrol | Sonuç |
|---|---|
| Qt 6 `lupdate` QField kaynak taraması | 1.445 etkin ileti |
| QField katalog–kaynak envanteri | 1.445 / 1.445; eksik 0, fazla 0 |
| QGIS Processing tam kaynak taraması | 3.885 ileti |
| QField yerinde-düzenleme Processing çalışma kümesi | 87 dosya, 726 ileti |
| Processing katalog–kaynak envanteri | 726 / 726; eksik 0, fazla 0 |
| Birleşik eklenti kataloğu | 2.169 / 2.169; eksik 0, fazla 0 |
| `unfinished` / boş çeviri | 0 / 0 |
| Qt yer tutucu uyuşmazlığı | 0 |
| HTML işaretleme uyuşmazlığı | 0 |
| Numerus yapısı | 39 birleşik ileti; hata 0 |
| Aynı kaynak için tutarsız çeviri | 0 |
| Bilinçli aynı bırakılan metin | 35; standart, birim, protokol veya Türkçede aynı sözcük |
| Qt 6 `lrelease` — çekirdek | Başarılı; 1.445 finished, 0 unfinished |
| Qt 6 `lrelease` — birleşik eklenti | Başarılı; 2.169 finished, 0 unfinished |
| Qt `QTranslator` çalışma zamanı testi | 7/7 geçti; çekirdek, Processing ve numerus aramaları |
| Derlenmiş QM sihirli bayt denetimi | Çekirdek ve ZIP içindeki iki QM için başarılı |
| `qmllint main.qml` | Başarılı |
| ZIP kökünde `main.qml` ve zorunlu dosyalar | Başarılı |
| `git diff --check` | Başarılı; hata 0 |
| Windows'ta QField uygulamasıyla kurulum | Test edilmedi; yürütülebilir QField bulunamadı |
| Android gerçek cihaz | Test edilmedi |
| iOS gerçek cihaz | Test edilmedi |
| APK / IPA derlemesi | Yapılmadı; SDK/NDK, macOS/Xcode ve imzalama yok |

`QTranslator` testi; “Harita Tuvali”, ağ terimi “Port”, “Tampon bölge
oluştur”, “Geometrileri ötele”, “Ortak sınırları kaldırarak birleştir”, “Alan
hesaplayıcı” ve Türkçe numerus aramasını derlenmiş `main_tr.qm` üzerinden
doğrulamıştır.

Bu sonuçlar katalog ve eklenti paketinin teknik bütünlüğünü kanıtlar. Gerçek
QField ekranlarında metin taşması, dokunma akışı, dosya izinleri, GNSS ve
QFieldCloud davranışı için platform kabul listesi ayrıca yürütülmelidir.

