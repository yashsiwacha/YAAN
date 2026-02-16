# Build script for YAAN Desktop Client

# Variables
$JAVAFX_PATH = "C:\javafx-sdk-17\lib"  # Update with your JavaFX path
$SRC_DIR = "src"
$BIN_DIR = "bin"
$LIB_DIR = "lib"

# Create bin directory if it doesn't exist
if (!(Test-Path $BIN_DIR)) {
    New-Item -ItemType Directory -Path $BIN_DIR | Out-Null
}

Write-Host "Compiling YAAN Desktop Client..." -ForegroundColor Green

# Compile Java files
javac --module-path $JAVAFX_PATH `
      --add-modules javafx.controls,javafx.fxml `
      -cp "$LIB_DIR\*" `
      -d $BIN_DIR `
      $SRC_DIR\*.java

if ($LASTEXITCODE -eq 0) {
    Write-Host "Compilation successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To run the application, use:" -ForegroundColor Cyan
    Write-Host ".\run.ps1" -ForegroundColor Yellow
} else {
    Write-Host "Compilation failed!" -ForegroundColor Red
    exit 1
}
