# YAAN One-Click Installer for Windows
# This script will install and set up YAAN automatically

param(
    [switch]$SkipTests = $false
)

$ErrorActionPreference = "Stop"

Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                           ║" -ForegroundColor Cyan
Write-Host "║         YAAN v1.0 - INSTALLER            ║" -ForegroundColor Cyan
Write-Host "║     Your AI Assistant Network            ║" -ForegroundColor Cyan
Write-Host "║                                           ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Cyan
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.10+ from:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    exit 1
}

$pythonVersion = python --version
Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green

# Check Python version
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
        Write-Host "❌ Python 3.10+ required, found: $pythonVersion" -ForegroundColor Red
        exit 1
    }
}

# Check if git is installed (optional but recommended)
Write-Host ""
Write-Host "[2/6] Checking Git installation..." -ForegroundColor Cyan
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "✓ Git found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Git not found (optional)" -ForegroundColor Yellow
}

# Create virtual environment
Write-Host ""
Write-Host "[3/6] Creating virtual environment..." -ForegroundColor Cyan
$venvPath = ".\backend\venv"

if (Test-Path $venvPath) {
    Write-Host "⚠️  Virtual environment already exists, skipping..." -ForegroundColor Yellow
} else {
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[4/6] Installing dependencies..." -ForegroundColor Cyan
& "$venvPath\Scripts\activate.ps1"

# Upgrade pip
python -m pip install --upgrade pip --quiet

# Install requirements
pip install -r .\backend\requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ All dependencies installed" -ForegroundColor Green

# Create necessary directories
Write-Host ""
Write-Host "[5/6] Setting up directories..." -ForegroundColor Cyan
$directories = @(
    ".\backend\data",
    ".\backend\logs",
    ".\backend\models"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "✓ Directories configured" -ForegroundColor Green

# Run tests
if (!$SkipTests) {
    Write-Host ""
    Write-Host "[6/6] Running tests..." -ForegroundColor Cyan
    Set-Location .\backend
    $testResult = python test_setup.py 2>&1
    Set-Location ..
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ All tests passed!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Some tests failed, but installation is complete" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "[6/6] Skipping tests..." -ForegroundColor Yellow
}

# Installation complete
Write-Host ""
Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                           ║" -ForegroundColor Green
Write-Host "║     ✅ YAAN INSTALLED SUCCESSFULLY!       ║" -ForegroundColor Green
Write-Host "║                                           ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Quick Start:" -ForegroundColor Cyan
Write-Host "   Run:  .\start.ps1" -ForegroundColor White
Write-Host "   Then open: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   README.md - Full documentation" -ForegroundColor White
Write-Host "   QUICKSTART.md - 5-minute guide" -ForegroundColor White
Write-Host ""
Write-Host "💡 Need help? Check the docs or visit:" -ForegroundColor Cyan
Write-Host "   https://github.com/yashsiwacha/YAAN" -ForegroundColor White
Write-Host ""
