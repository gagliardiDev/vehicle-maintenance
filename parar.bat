@echo off
setlocal
chcp 65001 > nul
cls
title AutoCare - Encerrar Servidor

cd /d "%~dp0"
set "PORT=8015"

echo ========================================================
echo       AUTOCARE // ENCERRANDO SERVIDOR (PORTA %PORT%)
echo ========================================================
echo.

echo [1/2] Encerrando processos na porta %PORT%...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /r /c:":%PORT% .*LISTENING"') do (
    echo Encerrando PID %%a...
    taskkill /F /PID %%a >nul 2>&1
)

ping 127.0.0.1 -n 2 >nul

echo [2/2] Verificando liberacao da porta %PORT%...
netstat -ano | findstr /r /c:":%PORT% .*LISTENING" >nul
if %errorlevel% equ 0 (
    echo [AVISO] Porta %PORT% ainda em uso. Tente executar este script como Administrador.
    exit /b 1
)

echo.
echo ========================================================
echo       SERVIDOR ENCERRADO COM SUCESSO! (PORTA %PORT% LIVRE)
echo ========================================================
ping 127.0.0.1 -n 2 >nul
exit /b 0
