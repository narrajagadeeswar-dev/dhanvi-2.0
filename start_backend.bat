@echo off
title DHANVI Healthcare Backend Server
echo ======================================================================
echo   Starting DHANVI Secure Backend Server (SQLite + RBAC + REST API)
echo ======================================================================
cd /d "%~dp0"
python server.py
pause
