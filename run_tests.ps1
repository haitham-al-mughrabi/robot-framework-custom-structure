# Robot Framework PowerShell Test Runner
# Universal cross-platform script for Windows, macOS, and Linux
param(
    [string]$TestPath = "Tests",
    [string]$Test = "",
    [string]$Suite = "",
    [string]$CaptchaSolver = "True",
    [string]$WindowFull = "False",
    [string]$WindowMaximized = "False",
    [switch]$Headless = $false,
    [switch]$Headed = $false,
    [string]$RunOffline = "False",
    [string]$DevTools = "False",
    [string]$ChromeSecuritySandbox = "False",
    [string]$PlaywrightTracing = "False",
    [string]$Environment = "uat",
    [string]$ExecutionEnv = "local",
    [string]$RecordVideo = "False",
    [string]$EnableHar = "False",
    [string]$WindowHeight = "1080",
    [string]$WindowWidth = "1920",
    [string]$ContextType = "NORMAL",
    [string]$LogLevel = "TRACE",
    [string]$ReportTitle = "Unified Automation Regression Testing Report",
    [switch]$MaximizeBrowser = $false,
    [switch]$AutoCloseBrowser = $true,
    [switch]$KeepVncOpen = $false,
    [switch]$FullWidthViewport = $false,
    [switch]$Help = $false
)

# Show usage information
if ($Help) {
    Write-Host @"

🤖 Robot Framework PowerShell Test Runner (Universal)

Usage: .\run_tests.ps1 [OPTIONS] [TEST_PATH]

GENERAL OPTIONS:
    -Help                      Show this help message

TEST SELECTION OPTIONS:
    -Test TEST_NAME           Run only tests matching this pattern
    -Suite SUITE_NAME         Run only suites matching this pattern
    -TestPath TEST_PATH       Path to test files (default: Tests)

BROWSER CONTROL OPTIONS:
    -MaximizeBrowser          Maximize browser window
    -FullWidthViewport        Use full screen width
    -AutoCloseBrowser         Auto-close browser after tests (default: True)
    -KeepVncOpen              Keep VNC session open after completion

EXECUTION OPTIONS:
    -Headless                 Run in headless mode
    -Headed                   Run in headed mode (shows browser)
    -Environment VALUE        Test environment (default: uat)
    -LogLevel VALUE           Robot Framework log level (default: TRACE)

EXAMPLES:
    # Run in headless mode
    .\run_tests.ps1 -Headless Tests\LoginTests.robot

    # Run specific test case
    .\run_tests.ps1 -Test "Login Test" Tests\

    # Run specific suite
    .\run_tests.ps1 -Suite "LoginSuite" Tests\

    # Run with maximized browser
    .\run_tests.ps1 -MaximizeBrowser Tests\LoginTests.robot

"@
    exit 0
}

# Configuration
$ImageName = "robot-framework-custom:latest"
$Platform = "linux/amd64"

# Determine execution mode
$UseDocker = $true
if ($env:REMOTE_CONTAINERS -or (Get-Location).Path -like "*robotframework*tests*") {
    Write-Host "🔍 Detected dev container environment - running tests directly"
    $UseDocker = $false
}

# Set headless based on switches
if ($Headed) { $HeadlessValue = "False" }
elseif ($Headless) { $HeadlessValue = "True" }
else { $HeadlessValue = "False" }

# Build Robot Framework arguments
$RobotArgs = @(
    "--pythonpath", ".",
    "--listener", "Resources/Setup/Listeners/KeywordListener.py",
    "--listener", "Resources/Setup/Listeners/LocatorFailureListener.py",
    "--loglevel", $LogLevel,
    "--variable", "CAPTCHA_SOLVER:$CaptchaSolver",
    "--variable", "WINDOW_FULL:$WindowFull",
    "--variable", "WINDOW_MAXIMIZED:$WindowMaximized",
    "--variable", "HEADLESS:$HeadlessValue",
    "--variable", "RUN_OFFLINE:$RunOffline",
    "--variable", "DEV_TOOLS:$DevTools",
    "--variable", "CHROME_SECURITY_SANDBOX:$ChromeSecuritySandbox",
    "--variable", "PLAYWRIGHT_TRACING:$PlaywrightTracing",
    "--variable", "DEVELOPMENT_ENVIRONMENT:$Environment",
    "--variable", "EXECUTION_ENV:$ExecutionEnv",
    "--variable", "RECORD_VIDEO:$RecordVideo",
    "--variable", "ENABLE_HAR:$EnableHar",
    "--variable", "WINDOW_HEIGHT:$WindowHeight",
    "--variable", "WINDOW_WIDTH:$WindowWidth",
    "--variable", "CONTEXT_TYPE:$ContextType",
    "--variable", "AUTO_CLOSE_BROWSER:$AutoCloseBrowser",
    "--outputdir", "Results/Reports/",
    "--splitlog",
    "--logtitle", $ReportTitle
)

# Add test/suite filters if specified
if ($Test) {
    $RobotArgs += "--test", $Test
}
if ($Suite) {
    $RobotArgs += "--suite", $Suite
}

# Add test path
$RobotArgs += $TestPath

# Display configuration
Write-Host "🤖 Robot Framework PowerShell Test Runner"
Write-Host "======================================="
Write-Host "📁 Test path: $TestPath"
if ($Test) { Write-Host "🎯 Test filter: $Test" }
if ($Suite) { Write-Host "📦 Suite filter: $Suite" }
Write-Host "🔧 Configuration:"
Write-Host " HEADLESS: $HeadlessValue"
Write-Host " ENVIRONMENT: $Environment"
Write-Host " LOG_LEVEL: $LogLevel"
Write-Host "======================================="

# Cleanup function for Windows
function Cleanup-VNC {
    Write-Host "🛑 Cleaning up VNC services..."

    # Stop processes using taskkill
    $processes = @("Xvfb", "x11vnc", "websockify")
    foreach ($proc in $processes) {
        try {
            Stop-Process -Name $proc -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped $proc processes"
        } catch {
            # Process not running, continue
        }
    }

    # Stop Docker containers
    try {
        $containers = docker ps -q --filter "ancestor=$ImageName" 2>$null
        if ($containers) {
            docker kill $containers 2>$null
            Write-Host "Stopped Docker containers"
        }
    } catch {
        # Docker not available or no containers running
    }
}

# Register cleanup on exit
Register-EngineEvent PowerShell.Exiting -Action { Cleanup-VNC } | Out-Null

# Cleanup existing processes
Cleanup-VNC

# Cross-platform volume mount handling
$CurrentDir = Get-Location
if ($IsWindows -or $env:OS -eq "Windows_NT") {
    # Windows path handling
    $VolumeMount = "${CurrentDir}:/opt/robotframework/tests"
} else {
    # Unix-like systems
    $VolumeMount = "${CurrentDir}:/opt/robotframework/tests:Z"
}

Write-Host "🔧 Platform: $([System.Environment]::OSVersion.Platform)"
Write-Host "📁 Volume mount: $VolumeMount"

# Execute based on mode
if (-not $UseDocker) {
    # Dev container mode
    Write-Host "🚀 Running Robot Framework tests directly in dev container..."

    # Create Results directory
    if (-not (Test-Path "Results/Reports")) {
        New-Item -ItemType Directory -Path "Results/Reports" -Force | Out-Null
    }

    # Run Robot Framework
    & python -m robot @RobotArgs

} elseif ($HeadlessValue -eq "True") {
    # Docker headless mode
    Write-Host "⚡ Running in headless mode..."

    $DockerArgs = @(
        "run", "--rm",
        "--platform", $Platform,
        "--shm-size=1g",
        "-v", $VolumeMount,
        $ImageName,
        "python", "-m", "robot"
    ) + $RobotArgs.Replace(".", "/opt/robotframework/tests").Replace("Results/Reports/", "/opt/robotframework/tests/Results/Reports/")

    & docker @DockerArgs

} else {
    # Docker headed mode with VNC
    Write-Host "🚀 Running in headed mode with live VNC viewing..."

    # Open VNC browser after delay
    Start-Job -ScriptBlock {
        Start-Sleep 10
        $VncUrl = "http://localhost:6080/vnc.html?autoconnect=true"
        Write-Host "🌐 Opening VNC viewer in browser..."
        Start-Process $VncUrl
    } | Out-Null

    $DockerArgs = @(
        "run", "--rm",
        "--platform", $Platform,
        "--shm-size=1g",
        "-p", "6080:6080",
        "-p", "5900:5900",
        "-v", $VolumeMount,
        "--entrypoint", "/bin/bash",
        $ImageName,
        "-c"
    )

    $BashScript = @"
echo '🔧 Setting up live VNC viewing...'
Xvfb :99 -screen 0 1920x1080x24 -ac -nolisten tcp -nolisten unix >/dev/null 2>&1 &
export DISPLAY=:99
sleep 3
x11vnc -display :99 -nopw -listen localhost -xkb -ncache 10 -ncache_cr -quiet -forever -rfbport 5900 >/dev/null 2>&1 &
websockify --web=/usr/share/novnc/ --wrap-mode=ignore 6080 localhost:5900 >/dev/null 2>&1 &
sleep 5
echo '🚀 VNC Live View Ready at http://localhost:6080'
cd /opt/robotframework/tests && python -m robot $($RobotArgs -join ' ' | ForEach-Object { $_ -replace 'Results/Reports/', '/opt/robotframework/tests/Results/Reports/' -replace '\.', '/opt/robotframework/tests' })
echo '🏁 Test execution completed!'
if (-not $KeepVncOpen) { sleep 5 } else { sleep 300 }
"@

    $DockerArgs += $BashScript
    & docker @DockerArgs
}

# Show results
Write-Host "✅ Test execution finished!"
Write-Host "📊 Results are available in: Results/Reports/"

if (Test-Path "Results/Reports/log.html") {
    Write-Host "📋 Log File: $(Resolve-Path 'Results/Reports/log.html')"
}
if (Test-Path "Results/Reports/report.html") {
    Write-Host "📊 Report File: $(Resolve-Path 'Results/Reports/report.html')"
}

Write-Host "💡 Tip: Open files above to view test results!"