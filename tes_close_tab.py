from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
            headless=False,
            executable_path="C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            args=["--disable-notifications", "--disable-logging"],
            slow_mo=5000
    )
    context = browser.new_context()    

    # Create some blank pages for demonstration
    try:
        for i in range(5):
            page = context.new_page()

            page.goto("https://my.telkomsel.com/login/web")
    finally:
        page.close()
        
    browser.close()