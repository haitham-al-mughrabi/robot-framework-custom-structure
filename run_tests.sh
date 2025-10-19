#!/bin/bash

set -e

# Function to cleanup VNC processes (cross-platform)
cleanup_vnc() {
    echo "🛑 Cleaning up VNC services..."

    # Detect platform and use appropriate cleanup method
    case "$(uname -s 2>/dev/null || echo Windows)" in
        CYGWIN*|MINGW*|MSYS*|Windows)
            # Windows cleanup
            if command -v taskkill >/dev/null 2>&1; then
                for proc in Xvfb x11vnc websockify; do
                    taskkill /F /IM "${proc}.exe" 2>/dev/null && echo "Stopped $proc processes" || true
                done
            elif command -v wmic >/dev/null 2>&1; then
                for proc in Xvfb x11vnc websockify; do
                    wmic process where "name='${proc}.exe'" delete 2>/dev/null && echo "Stopped $proc processes" || true
                done
            fi
            ;;
        *)
            # Unix-like systems (Linux, macOS, etc.)
            if command -v pkill >/dev/null 2>&1; then
                for proc in Xvfb x11vnc websockify; do
                    if pkill -f $proc 2>/dev/null; then
                        echo "Stopped $proc processes with pkill"
                    fi
                done
            elif command -v ps >/dev/null 2>&1; then
                for proc in Xvfb x11vnc websockify; do
                    pids=$(ps aux | grep $proc | grep -v grep | awk '{print $2}' 2>/dev/null)
                    if [ -n "$pids" ]; then
                        echo "Stopping $proc..."
                        echo $pids | xargs kill -9 2>/dev/null
                    fi
                done
            else
                echo "⚠️  No suitable process management tool found, skipping cleanup"
            fi
            ;;
    esac

    # Kill any Docker containers using VNC ports (cross-platform)
    if command -v docker >/dev/null 2>&1; then
        case "$(uname -s 2>/dev/null || echo Windows)" in
            CYGWIN*|MINGW*|MSYS*|Windows)
                # Windows Docker cleanup
                for container in $(docker ps -q --filter "ancestor=robot-framework-custom:latest" 2>/dev/null); do
                    docker kill "$container" 2>/dev/null && echo "Stopped Docker container $container"
                done
                ;;
            *)
                # Unix Docker cleanup
                docker ps -q --filter "ancestor=robot-framework-custom:latest" | xargs -r docker kill 2>/dev/null
                ;;
        esac
    fi
}

# Set trap to cleanup on script exit
trap cleanup_vnc EXIT INT TERM

# Check if running in dev container
if [[ -n "$REMOTE_CONTAINERS" ]] || [[ "$PWD" == "/opt/robotframework/tests" ]]; then
    echo "🔍 Detected dev container environment - running tests directly"
    USE_DOCKER=false
else
    echo "🐳 Running in local environment - using Docker"
    USE_DOCKER=true
    IMAGE_NAME="robot-framework-custom:latest"
fi

# Default values for all Robot Framework variables
TEST_PATHS="Tests"
CAPTCHA_SOLVER="True"
WINDOW_FULL="False"
WINDOW_MAXIMIZED="False"
HEADLESS="False"
RUN_OFFLINE="False"
DEV_TOOLS="False"
CHROME_SECURITY_SANDBOX="False"
PLAYWRIGHT_TRACING="False"
DEVELOPMENT_ENVIRONMENT="uat"
EXECUTION_ENV="local"
OMITCONTENT="False"
RECORD_VIDEO="False"
ENABLE_HAR="False"
WINDOW_HEIGHT="1080"
WINDOW_WIDTH="1920"
CONTEXT_TYPE="NORMAL"
LOG_LEVEL="TRACE"
REPORT_TITLE="Unified Automation Regression Testing Report"

# New options for browser control
MAXIMIZE_BROWSER="False"
AUTO_CLOSE_BROWSER="True"
KEEP_VNC_OPEN="False"
FULL_WIDTH_VIEWPORT="False"

# Robot Framework test/suite selection options
TEST_FILTER=""
SUITE_FILTER=""

# Function to show usage
show_usage() {
cat << EOF

🤖 Robot Framework Docker Test Runner with Enhanced Browser Control

Usage: $0 [OPTIONS] [TEST_PATH]

GENERAL OPTIONS:
    -v, --variable VAR:VALUE    Add custom Robot Framework variable (can be used multiple times)
    -h, --help                 Show this help message

TEST SELECTION OPTIONS:
    --test TEST_NAME           Run only tests matching this pattern
    --suite SUITE_NAME         Run only suites matching this pattern

BROWSER CONTROL OPTIONS:
    --maximize-browser         Maximize browser window (adds Maximize Window keyword)
    --full-width-viewport      Use full screen width (sets viewport=None)
    --auto-close-browser       Auto-close browser after tests (default: True)
    --keep-vnc-open           Keep VNC session open after completion (default: False)

ROBOT FRAMEWORK VARIABLES:
    --captcha-solver VALUE     Enable/disable CAPTCHA solver (True/False, default: True)
    --window-full VALUE        Enable/disable window full mode (True/False, default: False)
    --window-maximized VALUE   Enable/disable window maximize (True/False, default: False)
    --headless [VALUE]         Run in headless mode (True/False, default: True when flag used)
    --headed                   Run in headed mode (sets HEADLESS=False, shows browser with VNC in dev container)
    --run-offline VALUE        Enable/disable offline mode (True/False, default: False)
    --dev-tools VALUE          Enable/disable browser dev tools (True/False, default: False)
    --chrome-security-sandbox VALUE  Chrome security sandbox (True/False, default: False)
    --playwright-tracing VALUE Enable/disable Playwright tracing (True/False, default: False)
    --environment VALUE        Test environment (default: uat)
    --execution-env VALUE      Execution environment (default: local)
    --omit-content VALUE       Enable/disable content omission (True/False, default: False)
    --record-video VALUE       Enable/disable video recording (True/False, default: False)
    --enable-har VALUE         Enable/disable HAR capture (True/False, default: False)
    --window-height VALUE      Browser window height in pixels (default: 856)
    --window-width VALUE       Browser window width in pixels (default: 1528)
    --context-type VALUE       Browser context type (default: NORMAL)
    --log-level VALUE          Robot Framework log level (TRACE/DEBUG/INFO/WARN/ERROR, default: TRACE)

EXAMPLES:
    # Run in dev container with VNC viewing (headed mode)
    ./run_tests.sh --headed Tests/LoginTests.robot

    # Run in dev container headless mode
    ./run_tests.sh --headless Tests/LoginTests.robot

    # Run with maximized browser and auto-close
    ./run_tests.sh --maximize-browser Tests/LoginTests.robot

    # Run with full-width viewport (takes entire screen width)
    ./run_tests.sh --full-width-viewport Tests/ResponsiveTests.robot

    # Run and keep VNC open for manual inspection (Docker mode)
    USE_DOCKER=true ./run_tests.sh --keep-vnc-open Tests/DebugTests.robot

    # Run headless with custom window size
    ./run_tests.sh --headless --window-width 1920 --window-height 1080

    # Run with maximized browser, video recording, and auto-close
    ./run_tests.sh --maximize-browser --record-video True --auto-close-browser Tests/DemoTests.robot

    # Run only specific test case
    ./run_tests.sh --test "Login Test" Tests/

    # Run only specific suite
    ./run_tests.sh --suite "LoginSuite" Tests/

    # Run specific test in specific suite
    ./run_tests.sh --test "Login Test" --suite "LoginSuite" Tests/


EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --test)
      TEST_FILTER="$2"
      shift 2
      ;;
    --suite)
      SUITE_FILTER="$2"
      shift 2
      ;;
    --maximize-browser)
      MAXIMIZE_BROWSER="True"
      shift
      ;;
    --full-width-viewport)
      FULL_WIDTH_VIEWPORT="True"
      shift
      ;;
    --report-title)
      REPORT_TITLE="$2"
      shift 2
      ;;
    --auto-close-browser)
      AUTO_CLOSE_BROWSER="$2"
      shift 2
      ;;
    --keep-vnc-open)
      KEEP_VNC_OPEN="True"
      shift
      ;;
    --keep-vnc)
      KEEP_VNC_OPEN="True"
      shift
      ;;
    --captcha-solver)
      CAPTCHA_SOLVER="$2"
      shift 2
      ;;
    --window-full)
      WINDOW_FULL="$2"
      shift 2
      ;;
    --window-maximized)
      WINDOW_MAXIMIZED="$2"
      shift 2
      ;;
    --headless)
      if [[ "$2" && "$2" != --* ]]; then
        HEADLESS="$2"
        shift 2
      else
        HEADLESS="True"
        shift
      fi
      ;;
    --headed)
      HEADLESS="False"
      shift
      ;;
    --run-offline)
      RUN_OFFLINE="$2"
      shift 2
      ;;
    --dev-tools)
      DEV_TOOLS="$2"
      shift 2
      ;;
    --chrome-security-sandbox)
      CHROME_SECURITY_SANDBOX="$2"
      shift 2
      ;;
    --playwright-tracing)
      PLAYWRIGHT_TRACING="$2"
      shift 2
      ;;
    --environment)
      DEVELOPMENT_ENVIRONMENT="$2"
      shift 2
      ;;
    --execution-env)
      EXECUTION_ENV="$2"
      shift 2
      ;;
    --omit-content)
      OMITCONTENT="$2"
      shift 2
      ;;
    --record-video)
      RECORD_VIDEO="$2"
      shift 2
      ;;
    --enable-har)
      ENABLE_HAR="$2"
      shift 2
      ;;
    --window-height)
      WINDOW_HEIGHT="$2"
      shift 2
      ;;
    --window-width)
      WINDOW_WIDTH="$2"
      shift 2
      ;;
    --context-type)
      CONTEXT_TYPE="$2"
      shift 2
      ;;
    --log-level)
      LOG_LEVEL="$2"
      shift 2
      ;;
    -h|--help)
      show_usage
      exit 0
      ;;
    -*)
      echo "❌ Unknown option: $1"
      show_usage
      exit 1
      ;;
    *)
      # This is the test path
      TEST_PATHS="$1"
      shift
      ;;
  esac
done

# Build test/suite filter arguments
TEST_SUITE_ARGS=""
if [[ -n "$TEST_FILTER" ]]; then
  TEST_SUITE_ARGS="$TEST_SUITE_ARGS --test '$TEST_FILTER'"
fi
if [[ -n "$SUITE_FILTER" ]]; then
  TEST_SUITE_ARGS="$TEST_SUITE_ARGS --suite '$SUITE_FILTER'"
fi

# Cleanup any existing VNC processes to prevent port conflicts
echo "🧹 Cleaning up any existing VNC processes..."
cleanup_vnc

# Display configuration summary
echo "🤖 Robot Framework Docker Test Runner"
echo "======================================="
echo "📁 Test path: ${TEST_PATHS}"
if [[ -n "$TEST_FILTER" ]]; then
  echo "🎯 Test filter: ${TEST_FILTER}"
fi
if [[ -n "$SUITE_FILTER" ]]; then
  echo "📦 Suite filter: ${SUITE_FILTER}"
fi
echo "🔧 Browser Control:"
echo " HEADLESS: ${HEADLESS}"
echo " MAXIMIZE_BROWSER: ${MAXIMIZE_BROWSER}"
echo " FULL_WIDTH_VIEWPORT: ${FULL_WIDTH_VIEWPORT}"
echo " AUTO_CLOSE_BROWSER: ${AUTO_CLOSE_BROWSER}"
echo " KEEP_VNC_OPEN: ${KEEP_VNC_OPEN}"
echo "🔧 Configuration:"
echo " CAPTCHA_SOLVER: ${CAPTCHA_SOLVER}"
echo " WINDOW_FULL: ${WINDOW_FULL}"
echo " WINDOW_MAXIMIZED: ${WINDOW_MAXIMIZED}"
echo " RUN_OFFLINE: ${RUN_OFFLINE}"
echo " DEV_TOOLS: ${DEV_TOOLS}"
echo " CHROME_SECURITY_SANDBOX: ${CHROME_SECURITY_SANDBOX}"
echo " PLAYWRIGHT_TRACING: ${PLAYWRIGHT_TRACING}"
echo " DEVELOPMENT_ENVIRONMENT: ${DEVELOPMENT_ENVIRONMENT}"
echo " EXECUTION_ENV: ${EXECUTION_ENV}"
echo " OMITCONTENT: ${OMITCONTENT}"
echo " RECORD_VIDEO: ${RECORD_VIDEO}"
echo " ENABLE_HAR: ${ENABLE_HAR}"
echo " WINDOW_HEIGHT: ${WINDOW_HEIGHT}"
echo " WINDOW_WIDTH: ${WINDOW_WIDTH}"
echo " CONTEXT_TYPE: ${CONTEXT_TYPE}"
echo " LOG_LEVEL: ${LOG_LEVEL}"
echo "======================================="

# Cross-platform setup and architecture detection
HOST_ARCH=$(uname -m 2>/dev/null || echo "x86_64")
PLATFORM="linux/amd64"
HOST_OS=$(uname -s 2>/dev/null || echo "Windows")

# Detect current working directory with cross-platform compatibility
case "$HOST_OS" in
    CYGWIN*|MINGW*|MSYS*|Windows)
        # Windows path handling
        if [[ "$PWD" == /cygdrive/* ]]; then
            # Cygwin path - convert to Windows path for Docker
            CURRENT_DIR=$(cygpath -w "$PWD" 2>/dev/null || echo "$PWD")
        elif [[ "$PWD" == /[a-zA-Z]/* ]]; then
            # MSYS2/Git Bash path - convert to Windows path
            CURRENT_DIR="$(echo "$PWD" | sed 's|^/\([a-zA-Z]\)/|\1:/|')"
        else
            # Already Windows path or WSL path
            CURRENT_DIR="$PWD"
        fi
        VOLUME_MOUNT="$CURRENT_DIR:/opt/robotframework/tests"
        ;;
    *)
        # Unix-like systems (Linux, macOS)
        CURRENT_DIR="$(pwd)"
        VOLUME_MOUNT="$CURRENT_DIR:/opt/robotframework/tests:Z"
        ;;
esac

if [[ "${HOST_ARCH}" != "x86_64" ]]; then
  echo "Host is not x86_64. Forcing platform to ${PLATFORM} for compatibility."
else
  echo "Host is x86_64. Running on native platform: ${PLATFORM}."
fi

echo "🔧 Platform: $HOST_OS ($HOST_ARCH)"
echo "📁 Volume mount: $VOLUME_MOUNT"

# Function to open VNC URL in browser automatically
open_vnc_browser() {
  sleep 10 # Wait for VNC server to be fully ready
  VNC_URL="http://localhost:6080/vnc.html?autoconnect=true"
  echo "🌐 Opening VNC viewer in your browser..."
  # Detect OS and open browser accordingly
  case "$(uname)" in
    "Darwin") # macOS
      open "$VNC_URL" 2>/dev/null && echo "✅ Browser opened automatically!" || echo "⚠️ Please visit: $VNC_URL"
      ;;
    "Linux")
      if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$VNC_URL" 2>/dev/null && echo "✅ Browser opened automatically!" || echo "⚠️ Please visit: $VNC_URL"
      else
        echo "🌐 Please open this URL in your browser: $VNC_URL"
      fi
      ;;
    CYGWIN*|MINGW*|MSYS*) # Windows
      start "$VNC_URL" 2>/dev/null && echo "✅ Browser opened automatically!" || echo "⚠️ Please visit: $VNC_URL"
      ;;
    *)
      echo "🌐 Please open this URL in your browser: $VNC_URL"
      ;;
  esac
}

# Function to close VNC browser tab
close_vnc_browser() {
  if [[ "$KEEP_VNC_OPEN" == "False" ]]; then
    echo "🔒 Auto-closing VNC browser tab..."
    case "$(uname)" in
      "Darwin") # macOS
        osascript -e 'tell application "Safari" to close (every tab of every window whose URL contains "localhost:6080")' 2>/dev/null || \
        osascript -e 'tell application "Google Chrome" to close (every tab whose URL contains "localhost:6080")' 2>/dev/null || \
        echo "⚠️ Please manually close VNC browser tab"
        ;;
      *)
        echo "ℹ️ Please manually close VNC browser tab or it will close automatically"
        ;;
    esac
  fi
}

# 🎯 CONDITIONAL EXECUTION LOGIC
if [[ "$USE_DOCKER" == "false" ]]; then
  echo "🚀 Running Robot Framework tests directly in dev container..."

  # For headed mode in dev container, we need to setup display
  if [[ "$HEADLESS" == "False" ]]; then
    echo "🖥️ Setting up display for headed browser..."

    # Start Xvfb virtual display
    echo "🚀 Starting virtual display..."
    Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset >/dev/null 2>&1 &
    export DISPLAY=:99
    sleep 3

    # Start VNC server for viewing
    echo "🔗 Starting VNC server on :5900..."
    x11vnc -display :99 -nopw -listen 0.0.0.0 -xkb -ncache 10 -ncache_cr -forever -rfbport 5900 >/dev/null 2>&1 &
    sleep 2

    # Start noVNC web interface
    echo "🌐 Starting web VNC interface on :6080..."
    websockify --web=/usr/share/novnc/ --wrap-mode=ignore 6080 localhost:5900 >/dev/null 2>&1 &
    sleep 2
    echo "🌐 VNC available at: http://localhost:6080"
    echo "🖱️  Click 'Connect' when the page loads!"
  fi

  # Ensure Results/Reports directory exists
  mkdir -p Results/Reports

  # Run Robot Framework tests directly
  eval "python -m robot \
    --pythonpath . \
    --listener Resources/Setup/Listeners/KeywordListener.py \
    --listener Resources/Setup/Listeners/LocatorFailureListener.py \
    --loglevel ${LOG_LEVEL} \
    --variable CAPTCHA_SOLVER:${CAPTCHA_SOLVER} \
    --variable WINDOW_FULL:${WINDOW_FULL} \
    --variable WINDOW_MAXIMIZED:${WINDOW_MAXIMIZED} \
    --variable HEADLESS:${HEADLESS} \
    --variable RUN_OFFLINE:${RUN_OFFLINE} \
    --variable DEV_TOOLS:${DEV_TOOLS} \
    --variable CHROME_SECURITY_SANDBOX:${CHROME_SECURITY_SANDBOX} \
    --variable PLAYWRIGHT_TRACING:${PLAYWRIGHT_TRACING} \
    --variable DEVELOPMENT_ENVIRONMENT:${DEVELOPMENT_ENVIRONMENT} \
    --variable EXECUTION_ENV:${EXECUTION_ENV} \
    --variable OMITCONTENT:${OMITCONTENT} \
    --variable RECORD_VIDEO:${RECORD_VIDEO} \
    --variable ENABLE_HAR:${ENABLE_HAR} \
    --variable WINDOW_HEIGHT:${WINDOW_HEIGHT} \
    --variable WINDOW_WIDTH:${WINDOW_WIDTH} \
    --variable CONTEXT_TYPE:${CONTEXT_TYPE} \
    --variable AUTO_CLOSE_BROWSER:${AUTO_CLOSE_BROWSER} \
    --outputdir Results/Reports/ \
    --splitlog \
    --logtitle '${REPORT_TITLE}' \
    ${TEST_SUITE_ARGS} \
    '${TEST_PATHS}'"

  if [[ "$HEADLESS" == "False" ]]; then
    if [[ "$KEEP_VNC_OPEN" == "True" ]]; then
      echo "🌐 VNC still available at: http://localhost:6080"
      echo "Use ./stop_vnc.sh to stop VNC services manually"
    else
      echo "🛑 Cleaning up VNC services..."
      # Kill VNC processes
      for proc in Xvfb x11vnc websockify; do
          pids=$(ps aux | grep $proc | grep -v grep | awk '{print $2}' 2>/dev/null)
          if [ -n "$pids" ]; then
              echo "Stopping $proc..."
              echo $pids | xargs kill 2>/dev/null
          fi
      done
      echo "✅ VNC services stopped"
    fi
  fi

elif [[ "$HEADLESS" == "True" ]]; then
  echo "⚡ Running in headless mode - VNC server and browser opening skipped for faster execution"
  # Simple headless execution without VNC overhead
  eval "docker run --rm \
  --platform '${PLATFORM}' \
  --shm-size=1g \
  -v '${VOLUME_MOUNT}' \
  '${IMAGE_NAME}' \
  python -m robot \
  --pythonpath /opt/robotframework/tests \
  --listener /opt/robotframework/tests/Resources/Setup/Listeners/KeywordListener.py \
  --listener /opt/robotframework/tests/Resources/Setup/Listeners/LocatorFailureListener.py \
  --loglevel ${LOG_LEVEL} \
  --variable CAPTCHA_SOLVER:${CAPTCHA_SOLVER} \
  --variable WINDOW_FULL:${WINDOW_FULL} \
  --variable WINDOW_MAXIMIZED:${WINDOW_MAXIMIZED} \
  --variable HEADLESS:${HEADLESS} \
  --variable RUN_OFFLINE:${RUN_OFFLINE} \
  --variable DEV_TOOLS:${DEV_TOOLS} \
  --variable CHROME_SECURITY_SANDBOX:${CHROME_SECURITY_SANDBOX} \
  --variable PLAYWRIGHT_TRACING:${PLAYWRIGHT_TRACING} \
  --variable DEVELOPMENT_ENVIRONMENT:${DEVELOPMENT_ENVIRONMENT} \
  --variable EXECUTION_ENV:${EXECUTION_ENV} \
  --variable OMITCONTENT:${OMITCONTENT} \
  --variable RECORD_VIDEO:${RECORD_VIDEO} \
  --variable ENABLE_HAR:${ENABLE_HAR} \
  --variable WINDOW_HEIGHT:${WINDOW_HEIGHT} \
  --variable WINDOW_WIDTH:${WINDOW_WIDTH} \
  --variable CONTEXT_TYPE:${CONTEXT_TYPE} \
  --variable AUTO_CLOSE_BROWSER:${AUTO_CLOSE_BROWSER} \
  --outputdir /opt/robotframework/tests/Results/Reports/ \
  --splitlog \
  --logtitle '${REPORT_TITLE}' \
  ${TEST_SUITE_ARGS} \
  '${TEST_PATHS}'"
else
  echo "🚀 Running in headed mode with live VNC viewing..."
  # Start the background process to open browser
  open_vnc_browser &
  # Determine VNC session duration
  if [[ "$KEEP_VNC_OPEN" == "True" ]]; then
    VNC_WAIT_TIME="300" # 5 minutes
    VNC_MESSAGE="VNC session will remain open for 5 minutes for manual inspection..."
  else
    VNC_WAIT_TIME="5" # 5 seconds
    VNC_MESSAGE="VNC session closing in 5 seconds..."
  fi
  # Full VNC setup for live viewing
  docker run --rm \
  --platform "${PLATFORM}" \
  --shm-size=1g \
  -p 6080:6080 \
  -p 5900:5900 \
  -v "${VOLUME_MOUNT}" \
  --entrypoint /bin/bash \
  "${IMAGE_NAME}" \
  -c "
  echo '🔧 Setting up live VNC viewing...'
  # Start Xvfb (virtual display) - suppress warnings
  echo '🖥️ Starting virtual display...'
  Xvfb :99 -screen 0 1920x1080x24 -ac -nolisten tcp -nolisten unix >/dev/null 2>&1 &
  export DISPLAY=:99
  # Wait for Xvfb to initialize
  sleep 3
  # Start x11vnc server
  echo '🔗 Starting VNC server...'
  x11vnc -display :99 -nopw -listen localhost -xkb -ncache 10 -ncache_cr -quiet -forever -rfbport 5900 >/dev/null 2>&1 &
  # Start noVNC web interface
  echo '🌐 Starting web VNC interface...'
  websockify --web=/usr/share/novnc/ --wrap-mode=ignore 6080 localhost:5900 >/dev/null 2>&1 &
  # Wait for all services to be ready
  sleep 5
  echo '=============================================='
  echo '🚀 VNC Live View Ready!'
  echo '🌐 Browser should open automatically in ~10s'
  echo '🔗 Or manually visit: http://localhost:6080'
  echo '=============================================='
  # Run Robot Framework tests
  echo '🤖 Starting Robot Framework tests...'
  cd /opt/robotframework/tests && eval "python -m robot \
  --pythonpath /opt/robotframework/tests \
  --listener /opt/robotframework/tests/Resources/Setup/Listeners/KeywordListener.py \
  --listener /opt/robotframework/tests/Resources/Setup/Listeners/LocatorFailureListener.py \
  --loglevel ${LOG_LEVEL} \
  --variable CAPTCHA_SOLVER:${CAPTCHA_SOLVER} \
  --variable WINDOW_FULL:${WINDOW_FULL} \
  --variable WINDOW_MAXIMIZED:${WINDOW_MAXIMIZED} \
  --variable HEADLESS:${HEADLESS} \
  --variable RUN_OFFLINE:${RUN_OFFLINE} \
  --variable DEV_TOOLS:${DEV_TOOLS} \
  --variable CHROME_SECURITY_SANDBOX:${CHROME_SECURITY_SANDBOX} \
  --variable PLAYWRIGHT_TRACING:${PLAYWRIGHT_TRACING} \
  --variable DEVELOPMENT_ENVIRONMENT:${DEVELOPMENT_ENVIRONMENT} \
  --variable EXECUTION_ENV:${EXECUTION_ENV} \
  --variable OMITCONTENT:${OMITCONTENT} \
  --variable RECORD_VIDEO:${RECORD_VIDEO} \
  --variable ENABLE_HAR:${ENABLE_HAR} \
  --variable WINDOW_HEIGHT:${WINDOW_HEIGHT} \
  --variable WINDOW_WIDTH:${WINDOW_WIDTH} \
  --variable CONTEXT_TYPE:${CONTEXT_TYPE} \
  --variable AUTO_CLOSE_BROWSER:${AUTO_CLOSE_BROWSER} \
  --outputdir /opt/robotframework/tests/Results/Reports/ \
  --splitlog \
  --logtitle '${REPORT_TITLE}' \
  ${TEST_SUITE_ARGS} \
  '${TEST_PATHS}'"
  echo '🏁 Test execution completed!'
  echo '${VNC_MESSAGE}'
  sleep ${VNC_WAIT_TIME}
  "
  # Auto-close VNC browser tab if requested
  close_vnc_browser &
fi

# Function to display file links
show_results_links() {
  echo "✅ Test execution finished!"
  echo "📊 Results and Evidence Files:"
  echo "==============================================="

  # Detect if we're in Docker or dev container vs local machine
  if [[ "$USE_DOCKER" == "true" ]] || [[ "$PWD" == "/opt/robotframework/tests" ]]; then
    # Running in Docker - show commands to open files from host
    echo "🐳 Running in Docker - Use these commands from your HOST MAC TERMINAL:"
    echo "    (Open a new terminal on your Mac, navigate to this project folder, then run:)"
    echo ""

    # Show report files
    if [[ -f "Results/Reports/log.html" ]]; then
      echo "📋 Log File:"
      echo "   open Results/Reports/log.html"
    fi

    if [[ -f "Results/Reports/report.html" ]]; then
      echo "📊 Report File:"
      echo "   open Results/Reports/report.html"
    fi

    if [[ -f "Results/Reports/output.xml" ]]; then
      echo "🔧 Output XML:"
      echo "   open Results/Reports/output.xml"
    fi

    # Show video files if they exist
    if [[ -d "Results/Evidences/Video" ]]; then
      video_files=$(find Results/Evidences/Video -name "*.webm" 2>/dev/null)
      if [[ -n "$video_files" ]]; then
        echo "🎥 Video Recordings:"
        echo "   open Results/Evidences/Video/"
        latest_video=$(ls -t Results/Evidences/Video/*/*.webm 2>/dev/null | head -1)
        if [[ -n "$latest_video" ]]; then
          echo "   open \"$latest_video\"  # Latest video"
        fi
      fi
    fi

    # Show HAR files if they exist
    if [[ -f "Results/Evidences/HAR/har_file.har" ]]; then
      echo "🌐 HAR File:"
      echo "   open Results/Evidences/HAR/har_file.har"
    fi

    # Show tracing files if they exist
    if [[ -f "Results/Evidences/PlayRightTracingFile.zip" ]]; then
      echo "🕵️ Playwright Trace:"
      echo "   open Results/Evidences/PlayRightTracingFile.zip"
    fi

    echo ""
    echo "💡 IMPORTANT: Run these commands in your Mac terminal, NOT in this container!"
    echo "    1. Open Terminal.app on your Mac"
    echo "    2. cd to: $(echo $PWD | sed 's|/opt/robotframework/tests|/Users/TKM-h.almughrabi-c/Downloads/leanring_automation|')"
    echo "    3. Copy/paste the 'open' commands above"
    echo ""
    echo "🌐 OR start a web server to view everything in your browser:"
    echo "    ./serve_results.sh"
    echo "    Then open: http://localhost:8080"

  else
    # Running on local machine - show clickable file links
    echo "🏠 Local machine - Click links below to open files:"
    echo ""

    # Show report files
    if [[ -f "Results/Reports/log.html" ]]; then
      echo "📋 Log File: file://$(pwd)/Results/Reports/log.html"
    fi

    if [[ -f "Results/Reports/report.html" ]]; then
      echo "📊 Report File: file://$(pwd)/Results/Reports/report.html"
    fi

    if [[ -f "Results/Reports/output.xml" ]]; then
      echo "🔧 Output XML: file://$(pwd)/Results/Reports/output.xml"
    fi

    # Show video files if they exist
    if [[ -d "Results/Evidences/Video" ]]; then
      video_files=$(find Results/Evidences/Video -name "*.webm" 2>/dev/null)
      if [[ -n "$video_files" ]]; then
        echo "🎥 Video Recordings:"
        while IFS= read -r video_file; do
          echo "   📹 file://$(pwd)/$video_file"
        done <<< "$video_files"
        echo "📁 Video Folder: file://$(pwd)/Results/Evidences/Video"
      fi
    fi

    # Show HAR files if they exist
    if [[ -f "Results/Evidences/HAR/har_file.har" ]]; then
      echo "🌐 HAR File: file://$(pwd)/Results/Evidences/HAR/har_file.har"
    fi

    # Show tracing files if they exist
    if [[ -f "Results/Evidences/PlayRightTracingFile.zip" ]]; then
      echo "🕵️ Playwright Trace: file://$(pwd)/Results/Evidences/PlayRightTracingFile.zip"
    fi

    echo ""
    echo "💡 Tip: Cmd+Click links above to open files directly!"
  fi

  echo "==============================================="
}

show_results_links
