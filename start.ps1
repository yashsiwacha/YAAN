# YAAN Startup Script for Windows
# Run this to start the YAAN backend server

Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                           ║" -ForegroundColor Cyan
Write-Host "║   ██╗   ██╗ █████╗  █████╗ ███╗   ██╗   ║" -ForegroundColor Cyan
Write-Host "║   ╚██╗ ██╔╝██╔══██╗██╔══██╗████╗  ██║   ║" -ForegroundColor Cyan
Write-Host "║    ╚████╔╝ ███████║███████║██╔██╗ ██║   ║" -ForegroundColor Cyan
Write-Host "║     ╚██╔╝  ██╔══██║██╔══██║██║╚██╗██║   ║" -ForegroundColor Cyan
Write-Host "║      ██║   ██║  ██║██║  ██║██║ ╚████║   ║" -ForegroundColor Cyan
Write-Host "║      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ║" -ForegroundColor Cyan
Write-Host "║                                           ║" -ForegroundColor Cyan
Write-Host "║     Your AI Assistant Network v0.1.0     ║" -ForegroundColor Cyan
Write-Host "║          Offline • Private • Yours       ║" -ForegroundColor Cyan
Write-Host "║                                           ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found! Please install Python 3.10+" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Python found: $((python --version))" -ForegroundColor Green

# Check if virtual environment exists
$venvPath = ".\backend\venv"
if (!(Test-Path $venvPath)) {
    Write-Host ""
    Write-Host "📦 First time setup - Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $venvPath
    
    Write-Host "📥 Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    & "$venvPath\Scripts\activate.ps1"
    pip install --upgrade pip
    pip install -r .\backend\requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✓ Setup complete!" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
& "$venvPath\Scripts\activate.ps1"

# Run test (optional)
$runTest = Read-Host "Run tests first? (y/N)"
if ($runTest -eq "y" -or $runTest -eq "Y") {
    Write-Host ""
    Write-Host "🧪 Running tests..." -ForegroundColor Cyan
    python .\backend\test_setup.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Tests failed! Please check the errors above." -ForegroundColor Red
        exit 1
    }
}

# Start server
Write-Host ""
Write-Host "🚀 Starting YAAN backend server..." -ForegroundColor Green
Write-Host "   Server will be available at: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

Set-Location .\backend
python main.py
