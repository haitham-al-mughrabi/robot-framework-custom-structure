browser_arguments = {
    "shared": [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--enable-webgl",
        "--ignore-gpu-blacklist",
        "--disable-infobars",
        '--use-gl=swiftshader',
        '--enable-webgl',
        "--no-first-run"
    ],
    "local": [

    ],
    "pipeline": [
        "--headless=new",
    ]
}

FIREFOX_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
APPLE_WEB_KIT_AGENT = "AppleWebKit/537.36 (KHTML, like Gecko)"
CHROME_AGENT = "Chrome/131.0.0.0"
SAFARI_AGENT = "Safari/537.36"
EDGE_AGENT = "Edg/131.0.0.0"

BROWSER_AGENT = f"{FIREFOX_AGENT} {APPLE_WEB_KIT_AGENT} {CHROME_AGENT} {SAFARI_AGENT} {EDGE_AGENT}"
