@echo off
REM Universal Robot Framework Test Runner Wrapper for Windows
REM This script automatically detects available tools and runs the appropriate version

setlocal enabledelayedexpansion

echo 🤖 Universal Robot Framework Test Runner (Windows)
echo =====================================================

REM Check for PowerShell (preferred)
where pwsh >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ Found PowerShell Core (pwsh), using PowerShell runner
    pwsh -ExecutionPolicy Bypass -File "%~dp0run_tests.ps1" %*
    goto :end
)

where powershell >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ Found Windows PowerShell, using PowerShell runner
    powershell -ExecutionPolicy Bypass -File "%~dp0run_tests.ps1" %*
    goto :end
)

REM Check for WSL (Windows Subsystem for Linux)
where wsl >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ Found WSL, using bash runner
    wsl bash "%~dp0run_tests.sh" %*
    goto :end
)

REM Check for Git Bash
where bash >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ Found bash, using bash runner
    bash "%~dp0run_tests.sh" %*
    goto :end
)

REM Fallback: Basic Docker execution
where docker >nul 2>nul
if %errorlevel% equ 0 (
    echo ⚠️  No PowerShell/Bash found, using basic Docker execution
    echo 🐳 Running basic headless test...
    set TEST_PATH=Tests
    if not "%1"=="" set TEST_PATH=%1

    docker run --rm --platform linux/amd64 --shm-size=1g -v "%CD%:/opt/robotframework/tests" robot-framework-custom:latest python -m robot --pythonpath /opt/robotframework/tests --outputdir /opt/robotframework/tests/Results/Reports/ !TEST_PATH!

    echo ✅ Basic test execution completed!
    echo 📁 Results available in: Results\Reports\
    if exist "Results\Reports\log.html" echo 📋 Log: Results\Reports\log.html
    if exist "Results\Reports\report.html" echo 📊 Report: Results\Reports\report.html
    goto :end
) else (
    echo ❌ No suitable execution environment found!
    echo.
    echo Please install one of the following:
    echo   • PowerShell Core: https://github.com/PowerShell/PowerShell
    echo   • Git for Windows (includes bash): https://git-scm.com/download/win
    echo   • Windows Subsystem for Linux: https://docs.microsoft.com/en-us/windows/wsl/install
    echo   • Docker Desktop: https://www.docker.com/products/docker-desktop
    exit /b 1
)

:end
echo.
echo 🎉 Execution completed! Check the output above for results.