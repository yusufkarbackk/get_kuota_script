import json
import os
from playwright.sync_api import sync_playwright
import sys

client = sys.argv[1]
password = sys.argv[2]
number = sys.argv[3]
# chrome_profile = sys.argv[4]
company = sys.argv[4]
team_flag = sys.argv[5]

# client = "sxtstock1"
# password = "batiku232"
# number = "081119026097"
# # chrome_profile = "52"
# company = "sxtstock1"
# team_flag = "bati"

profile_dir = (
    f"/Users/yusufkarback/Library/Application Support/Google/Chrome/profile-{client}"
)
chrome_profile = f"profile-{client}"
# Check if the directory exists, if not, create it
remove_popup = 1
if not os.path.exists(profile_dir):
    # print("create new profile")
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
            # print("already logged in: halaman detail kuota")
            page.goto("https://my.telkomsel.com/detail-quota/internet")
            span_text = page.text_content("span.QuotaDetail__style__t1")
            trimmed_text = span_text.split()[0]
            # print(float(trimmed_text))
            with open(
                "/Users/yusufkarback/ambis/selenium_basic/new_akun_twt.txt", "a"
            ) as file:
                file.write(f"{chrome_profile},{client},{password}\n")
            sukses = True
            # print("sukses true")
            browser.close()
        else:
            # time.sleep(120)
            # print("not logged in")

            page.click("div.DialogInstallPWADesktop__style__closeIcon")

            page.click('text="Lanjutkan di Web"')
            page.click('text="Masuk dengan metode lain"')
            # page.click('text="Lanjutkan di Web"')
            page.click('text="Masuk Dengan Twitter"')

            page.click("#allow")
            page.click("#allow")
            # page.locator("span:has-text('Sign in to X')").wait_for()

            # print("masukin usernae")
            page.locator('input[name="text"]').fill(client)
            page.click('text="Next"')
            page.locator('input[name="password"]').fill(password)
            page.click('text="Log in"')

            page.wait_for_selector("div.HeaderNavigationV2__style__profile")

            page.goto("https://my.telkomsel.com/detail-quota/internet")
            span_text = page.text_content("span.QuotaDetail__style__t1")
            trimmed_text = span_text.split()[0]
            # print(float(trimmed_text))
            with open(
                "/Users/yusufkarback/ambis/selenium_basic/new_akun_twt.txt", "a"
            ) as file:
                file.write(f"{chrome_profile},{client},{password}\n")
            sukses = True
            # print("sukses true")
            browser.close()

data = {
    "quota": float(trimmed_text),
    "chrome_profile": chrome_profile,
    "profile_path": profile_dir,
}
print(json.dumps(data))
sys.stdout.flush()
