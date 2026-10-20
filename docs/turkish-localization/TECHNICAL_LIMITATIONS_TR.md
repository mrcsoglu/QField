# Teknik uygulanabilirlik ve sınırlamalar

## Kaynak kodu sonucu

QField 4.3.6 etiketi `d093eeba97c1a791b93ab1d059c91c7c57ec79cf`
commit'idir. `QfAppInterface` bu sürümde `availableLanguages()` ve
`changeLanguage()` işlevlerini sunar. Birincisi yalnızca `:/i18n/qfield_*.qm`
gömülü kaynaklarını listeler; ikincisi yalnızca bu listedeki dillere geçer,
QField ve Qt çeviricilerini yeniden kurar ve `QQmlEngine::retranslate()` çağırır.

`QfPluginManager::loadPlugin()` ise etkin yerel ayara göre `main_<locale>.qm`
dosyasını yükler ve `QCoreApplication::installTranslator()` ile uygulama
düzeyinde kurar. Qt çeviricileri ters kurulum sırasıyla arandığından, aynı
bağlam ve kaynak metinlerini taşıyan `main_tr.qm`, başlangıçta gömülü eksik
Türkçe kataloğu güvenli biçimde tamamlayabilir. QML nesnesi arama veya çalışma
zamanı metin değiştirme hilesi kullanılmaz.

QField'in sabitlediği QGIS kaynağı
`3a92eb30c83d7d52751a330628d72b8eb9e64876` commit'idir. QField'in Processing
modeli Native sağlayıcıyı yükler ve yalnızca `SupportsInPlaceEdits` yeteneğine
sahip algoritmaları, desteklenen parametre türleriyle birlikte gösterir. Bu
commit'in `src/analysis/processing` ve `src/core/processing` ağaçlarının tamamı
tarandığında 3.885 kaynak iletisi bulundu. Yerinde düzenleme sınıflarından ve
yeteneği açıkça bildiren uygulamalardan oluşan 87 kaynak dosyalık çalışma kümesi
726 etkin ileti içerir; algoritma adı, grup adı, parametre, seçenek, kısa yardım,
uzun açıklama ve hata metinleri bu katalogda çevrilmiştir. QGIS çalışma zamanı
sağlayıcısı bu Windows ortamında ayrıca örneklenemediği için 726 kayıt kaynak
kodundan çıkarılmış statik çalışma kümesidir; bu sınırlama cihaz testiyle
karıştırılmamalıdır.

Bu kullanım 4.3.6 kaynak davranışına dayanır; belgelenmiş eklenti sözleşmesi
yalnızca eklentinin kendi metinlerinin çevrilmesini taahhüt eder ve resmî en iyi
uygulamalar eklentilerin çekirdek davranışı geçersiz kılmamasını önerir. Bu
nedenle ZIP pratik bir 4.3.6 dağıtım seçeneğidir, ileri sürümler için API
garantisi değildir. Kalıcı ve upstream tarafından desteklenen çözüm tamamlanan
`i18n/qfield_tr.ts` kataloğunun resmî uygulamaya alınmasıdır.

## Bilinen sınır

QField 4.3.6 çalışma sırasında dil değiştirirken yüklü eklenti çeviricilerini
yeniden kurmaz. Böylece yerleşik QField çeviricisi yeniden en yüksek önceliği
alır. Dil Türkçe seçildikten sonra uygulamayı yeniden başlatmak bu durumu
düzeltir. Sürdürülebilir çekirdek iyileştirmesi, dil değişiminden sonra etkin
eklenti çeviricilerini yeni `QLocale` ile yeniden yükleyip bundan sonra
`QQmlEngine::retranslate()` çağırmaktır.

Eklentiler QML/JavaScript üzerinden QField'in açtığı bağlam nesnelerine erişir;
işletim sistemi yetkilerini aşmaz. Android/iOS dosya, konum, kamera vb. izinleri
uygulamanın platform izinleriyle sınırlıdır.

Bu paket QField kaynak metinleri ile QField'in yerinde düzenleme ekranında
kullandığı QGIS Native Processing çalışma kümesini kapsar. Qt'nin kendi standart
iletişim kutuları, QGIS'in QField tarafından gösterilmeyen masaüstü arayüzü ve
üçüncü taraf sağlayıcı eklentileri kendi çeviri kataloglarına bağlıdır.

