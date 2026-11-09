@echo off
setlocal
chcp 65001 > nul
cls
title AutoCare - Controle de Manutenção Veicular (FastAPI + Vue 3)

echo ========================================================
echo       AUTOCARE - CONTROLE DE MANUTENÇÃO VEICULAR
echo          Suzuki SX4 4WD ^& Honda Biz 125 2011
echo ========================================================
echo.

cd /d "%~dp0"
set "PYTHONPATH=%CD%"
set "PORT=8015"

:: Liberar porta se ja estiver ocupada por instancia anterior
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r /c:":%PORT% .*LISTENING"') do (
    echo [AVISO] Porta %PORT% em uso pelo processo PID %%a. Encerrando instancia anterior...
    taskkill /F /PID %%a >nul 2>&1
    ping 127.0.0.1 -n 2 >nul
)

:: Descobrir o IP local Wi-Fi / Ethernet
set "LOCAL_IP="
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4" ^| findstr /v "127.0.0.1" ^| findstr /v "169.254"') do (
    if not defined LOCAL_IP set "LOCAL_IP=%%i"
)
if defined LOCAL_IP set "LOCAL_IP=%LOCAL_IP: =%"
if not defined LOCAL_IP set "LOCAL_IP=127.0.0.1"

echo ========================================================
echo [PC] ACESSO NO COMPUTADOR:
echo    http://localhost:%PORT%
echo.
echo [WI-FI] ACESSO NO CELULAR ^(na mesma rede Wi-Fi^):
echo    http://%LOCAL_IP%:%PORT%
echo.
echo [DOCS] DOCUMENTAÇÃO SWAGGER ^(APIs REST^):
echo    http://localhost:%PORT%/docs
echo.
echo [DB] BANCO DE DADOS LOCAL:
echo    data\maintenance.db
echo ========================================================
echo.
echo Pressione Ctrl+C para encerrar o servidor.
echo.

python -m uvicorn src.main:app --host 0.0.0.0 --port %PORT%
