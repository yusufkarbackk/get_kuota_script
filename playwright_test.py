import os
from playwright.sync_api import sync_playwright
import sys
import db

client = sys.argv[1]
password = sys.argv[2]
number = sys.argv[3]
chrome_profile = sys.argv[4]
company = sys.argv[5]
team_flag = sys.argv[6]

profile_dir = (
    f"/Users/yusufkarback/Library/Application Support/Google/Chrome/{chrome_profile}"
)

# Check if the directory exists, if not, create it
remove_popup = 1
if not os.path.exists(profile_dir):
    print("create new profile")
    os.makedirs(profile_dir)
sukses = False
while sukses == False:

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            headless=False,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            user_data_dir=profile_dir,
            args=["--disable-notifications"],
        )
        page = browser.new_page()
        page.goto("https://my.telkomsel.com/login/web")

        profile_div = page.locator("div.HeaderNavigationV2__style__profile")
        if profile_div.is_visible():
            print("already logged in: halaman detail kuota")
            page.goto("https://my.telkomsel.com/detail-quota/internet")
            span_text = page.text_content("span.QuotaDetail__style__t1")
            trimmed_text = span_text.split()[0]
            print(float(trimmed_text))
            db.insert_client(
                client,
                company,
                team_flag,
                number,
                float(trimmed_text),
                chrome_profile,
                profile_dir,
            )
            browser.close()
            break
        else:
            # time.sleep(120)
            print("not logged in")

            page.click("div.DialogInstallPWADesktop__style__closeIcon")

            page.click('text="Lanjutkan di Web"')
            page.click('text="Masuk dengan metode lain"')
            # page.click('text="Lanjutkan di Web"')
            page.click('text="Masuk Dengan Twitter"')
            print("masukin usernae")
            page.fill("input[name='session[username_or_email]']", "sxtstock1")
            print("masukin password")
            page.fill("input[name='session[password]']", "batiku232")
            page.click(
                'input[type="checkbox"]#remember'
            )  # Selects the checkbox by ID 'remember'

            page.click("#allow")
            page.wait_for_selector(
                "div.HeaderNavigationV2__style__profile"
            )  # Replace with the correct selector for the element
