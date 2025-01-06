from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Launch the browser and open a page
    browser = p.chromium.launch(
            headless=False,
            executable_path="C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            args=["--disable-notifications", "--disable-logging"],
            slow_mo=1000
        )    
    page = browser.new_page()
    page.goto("https://www.mybaticloud.com/aboutus/")  # Replace with your URL
 # Find the span with the 'data-metadata' attribute
    element = page.query_selector('data-metadata')  # Selects <span> with 'data-metadata'

    # If you want to interact with it or get its text
    if element:
        print("Element found:", element.text_content())
    else:
        print("Element not found")

    # Close the browser
    browser.close()