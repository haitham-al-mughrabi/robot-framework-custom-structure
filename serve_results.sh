#!/bin/bash

# Simple web server to view test results and videos in browser
set -e

PORT="${1:-8080}"
RESULTS_DIR="Results"

echo "🌐 Starting local web server to view test results..."
echo "========================================================"

# Check if Results directory exists
if [[ ! -d "$RESULTS_DIR" ]]; then
    echo "❌ Results directory not found. Run tests first to generate results."
    exit 1
fi

# Create a simple index.html for navigation
cat > "${RESULTS_DIR}/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robot Framework Test Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
        .section { margin: 20px 0; padding: 15px; border-left: 4px solid #4CAF50; background: #f9f9f9; }
        .section h2 { margin-top: 0; color: #555; }
        a { color: #4CAF50; text-decoration: none; display: inline-block; margin: 5px 10px 5px 0; padding: 8px 12px; background: #e8f5e8; border-radius: 4px; }
        a:hover { background: #4CAF50; color: white; }
        .video-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin-top: 15px; }
        .video-item { text-align: center; }
        .video-item video { width: 100%; max-width: 200px; height: 120px; border-radius: 4px; }
        .no-files { color: #999; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Robot Framework Test Results</h1>

        <div class="section">
            <h2>📊 Test Reports</h2>
            <div id="reports"></div>
        </div>

        <div class="section">
            <h2>🎥 Video Recordings</h2>
            <div id="videos"></div>
        </div>

        <div class="section">
            <h2>🔧 Debug Files</h2>
            <div id="debug"></div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Page loaded, generating file links...');

            // Simply add all possible links and let the browser handle them
            const reportsContainer = document.getElementById('reports');
            reportsContainer.innerHTML = `
                <a href="Reports/report.html" target="_blank">📊 Test Report</a>
                <a href="Reports/log.html" target="_blank">📋 Detailed Log</a>
                <a href="Reports/output.xml" target="_blank">🔧 XML Output</a>
            `;

            const debugContainer = document.getElementById('debug');
            debugContainer.innerHTML = `
                <a href="Evidences/HAR/har_file.har" target="_blank">🌐 HAR File</a>
                <a href="Evidences/PlayRightTracingFile.zip" target="_blank">🕵️ Playwright Trace</a>
            `;

            const videosContainer = document.getElementById('videos');
            videosContainer.innerHTML = `
                <a href="Evidences/Video/" target="_blank">📁 Browse Video Directory</a>
                <div class="video-grid" style="margin-top: 15px;">
                    <div class="video-item">
                        <p>Video files in Evidences/Video/:</p>
                        <a href="Evidences/Video/Verify/" target="_blank">📁 Verify Test Videos</a>
                    </div>
                </div>
            `;
        });
    </script>
</body>
</html>
EOF

echo "📁 Created navigation page at: Results/index.html"
echo ""

# Check if Python 3 is available for web server
if command -v python3 >/dev/null 2>&1; then
    echo "🚀 Starting Python web server on port $PORT..."
    echo "🌐 Open your browser to: http://localhost:$PORT"
    echo ""
    echo "Available pages:"
    echo "  📋 Main Navigation: http://localhost:$PORT"
    if [[ -f "Results/Reports/report.html" ]]; then
        echo "  📊 Test Report: http://localhost:$PORT/Reports/report.html"
    fi
    if [[ -f "Results/Reports/log.html" ]]; then
        echo "  📋 Detailed Log: http://localhost:$PORT/Reports/log.html"
    fi
    if [[ -d "Results/Evidences/Video" ]]; then
        echo "  🎥 Videos: http://localhost:$PORT/Evidences/Video/"
    fi
    echo ""
    echo "💡 Press Ctrl+C to stop the server"
    echo "========================================================"

    cd "$RESULTS_DIR"
    python3 -m http.server "$PORT"
else
    echo "❌ Python 3 not found. Please install Python 3 to use the web server."
    echo "   Alternatively, you can:"
    echo "   - Open Results/index.html directly in your browser"
    echo "   - Use the 'open' commands provided by the test runner"
    exit 1
fi