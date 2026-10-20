# Android dağıtımı

## Resmî QField uygulaması

1. Ayarlar > Dil bölümünde Türkçeyi seçin.
2. Eklenti Yöneticisi > URL'den eklenti kur yoluyla
   `qfield-turkce-2.0.0.zip` dosyasını kurun.
3. Eklentiyi etkinleştirin, QField'ı son uygulamalar ekranından tamamen kapatın
   ve yeniden açın.
4. Kaldırırken eklenti yöneticisini kullanıp uygulamayı yeniden başlatın.

Yerel dosya URL'sinin cihaz/Android sürümünde kabul edilmemesi hâlinde ZIP'i
HTTPS üzerinden erişilebilir bir konuma koyun. ZIP kökünde `main.qml` bulunur.

## Kaynaktan APK

Güncellenmiş `i18n/qfield_tr.ts` standart QField CMake işlemiyle gömülür.
Resmî Android derleme bağımlılıklarını ve imzalama ayarlarını izleyin. Resmî
uygulamayla yan yana kurulum için uygulama kimliği, ad ve imzalama anahtarı ayrı
olmalıdır. Bu çalışma ortamında Android SDK/NDK ve imzalama anahtarı bulunmadığı
için APK üretilmemiştir.

