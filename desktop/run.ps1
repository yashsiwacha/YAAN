# Run script for YAAN Desktop Client

# Variables
$JAVAFX_PATH = "C:\javafx-sdk-17\lib"  # Update with your JavaFX path
$BIN_DIR = "bin"
$LIB_DIR = "lib"

Write-Host "Starting YAAN Desktop Client..." -ForegroundColor Green

# Run the application
java --module-path $JAVAFX_PATH `
     --add-modules javafx.controls,javafx.fxml `
     -cp "$BIN_DIR;$LIB_DIR\*" `
     YAANClient

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start application!" -ForegroundColor Red
    exit 1
}
