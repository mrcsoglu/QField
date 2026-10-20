# QField 4.3.6 Türkçe yerelleştirme

Bu dal, QField 4.3.6 kaynak envanteriyle eşitlenmiş Türkçe Qt kataloğunu,
QField'in kullandığı QGIS Native Processing işlemlerinin Türkçe kataloğunu,
uygulama geneli dil paketi dağıtımını ve otomatik kalite kontrollerini içerir.

## Hızlı kullanım

- Resmî uygulama: `distribution/qfield-turkce` içeriğinden üretilen ZIP'i kurun,
  dili Türkçe seçin ve uygulamayı yeniden başlatın.
- Özel derleme: güncellenmiş `i18n/qfield_tr.ts` dosyasını normal QField CMake
  derlemesinde kullanın. `src/app/CMakeLists.txt` tüm `i18n/*.ts` dosyalarını
  Qt 6 `lrelease` ile derleyip `:/i18n` kaynağına gömer.

## Doğrulama

```powershell
python scripts/i18n/validate_ts.py i18n/qfield_tr.ts --strict
python scripts/i18n/validate_ts.py i18n/qgis_processing_tr.ts --strict
pwsh scripts/i18n/build_turkish_package.ps1 -LRelease C:\Qt\6.x\bin\lrelease.exe -Version 2.0.0
```

Ayrıntılar için `docs/turkish-localization/` dizinine bakın.

