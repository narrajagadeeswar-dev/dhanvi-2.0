# PowerShell Launcher for DHANVI Backend Server
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  Starting DHANVI Secure Backend Server (SQLite + RBAC + REST API)" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan

Set-Location -Path $PSScriptRoot
python server.py
