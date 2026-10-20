param(
  [Parameter(Mandatory = $true)]
  [string]$LRelease,
  [string]$Python = "python",
  [string]$OutputDirectory = "build/turkish-localization-2.0.0",
  [string]$Version = "2.0.0"
)

$ErrorActionPreference = "Stop"
$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$coreCatalog = Join-Path $repositoryRoot "i18n/qfield_tr.ts"
$processingCatalog = Join-Path $repositoryRoot "i18n/qgis_processing_tr.ts"
$pluginSource = Join-Path $repositoryRoot "distribution/qfield-turkce"
$output = if ([System.IO.Path]::IsPathRooted($OutputDirectory)) {
  $OutputDirectory
} else {
  Join-Path $repositoryRoot $OutputDirectory
}
$pluginStage = Join-Path $output "qfield-turkce"

New-Item -ItemType Directory -Force -Path $output, $pluginStage | Out-Null

& $Python (Join-Path $PSScriptRoot "manual_tr_review.py") $coreCatalog
if ($LASTEXITCODE -ne 0) { throw "QField review application failed" }
& $Python (Join-Path $PSScriptRoot "manual_processing_review.py") $processingCatalog
if ($LASTEXITCODE -ne 0) { throw "Processing review application failed" }

& $Python (Join-Path $PSScriptRoot "validate_ts.py") $coreCatalog --strict --json (Join-Path $output "qfield-validation.json")
if ($LASTEXITCODE -ne 0) { throw "QField TS validation failed" }
& $Python (Join-Path $PSScriptRoot "validate_ts.py") $processingCatalog --strict --json (Join-Path $output "qgis-processing-validation.json")
if ($LASTEXITCODE -ne 0) { throw "Processing TS validation failed" }

Copy-Item -Force (Join-Path $pluginSource "main.qml") $pluginStage
Copy-Item -Force (Join-Path $pluginSource "metadata.txt") $pluginStage
Copy-Item -Force (Join-Path $pluginSource "README_TR.md") $pluginStage

$mergedCatalog = Join-Path $pluginStage "main_tr.ts"
& $Python (Join-Path $PSScriptRoot "merge_ts.py") $coreCatalog $processingCatalog --output $mergedCatalog
if ($LASTEXITCODE -ne 0) { throw "Catalog merge failed" }
& $Python (Join-Path $PSScriptRoot "validate_ts.py") $mergedCatalog --strict --json (Join-Path $output "merged-validation.json")
if ($LASTEXITCODE -ne 0) { throw "Merged TS validation failed" }

& $LRelease $coreCatalog -qm (Join-Path $output "qfield_tr.qm")
if ($LASTEXITCODE -ne 0) { throw "qfield_tr.qm compilation failed" }
& $LRelease $mergedCatalog -qm (Join-Path $pluginStage "main_tr.qm")
if ($LASTEXITCODE -ne 0) { throw "main_tr.qm compilation failed" }
Copy-Item -Force (Join-Path $pluginStage "main_tr.qm") (Join-Path $pluginStage "main_tr_TR.qm")

$zip = Join-Path $output "qfield-turkce-$Version.zip"
if (Test-Path -LiteralPath $zip) { Remove-Item -LiteralPath $zip }
Compress-Archive -Path (Join-Path $pluginStage "*") -DestinationPath $zip

$entries = [System.IO.Compression.ZipFile]::OpenRead($zip).Entries.FullName
foreach ($required in @("main.qml", "metadata.txt", "main_tr.qm", "main_tr_TR.qm", "main_tr.ts", "README_TR.md")) {
  if ($entries -notcontains $required) { throw "ZIP root does not contain $required" }
}
Write-Output $zip

