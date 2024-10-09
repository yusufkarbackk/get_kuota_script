import json
import os
from playwright.sync_api import sync_playwright
import sys
import db
import datetime

Y = datetime.date.today().year
M = datetime.date.today().month
D = datetime.date.today().day


with open("/Users/yusufkarback/ambis/selenium_basic/new_akun_twt.txt") as profiles:
    for profile in profiles:
        profiles = profile.strip().split(",")
        if len(profiles) != 3:
            print(f"Invalid profile format: {profile}")
            continue

        profile_name, username, password = profiles
        print(profile_name)
        print(username)
        print(password)
        profile_dir = f"/Users/yusufkarback/Library/Application Support/Google/Chrome/{profile_name}"
        # Check if the directory exists, if not, create it
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
                    nomor = page.text_content("span.StatusInfo__style__number")

                    page.goto("https://my.telkomsel.com/detail-quota/internet")
                    kuota = page.text_content("span.QuotaDetail__style__t1")
                    trimmed_kuota = kuota.split()[0]
                    trimmed_nomor = nomor.replace(" ", "")
                    sukses = True
                    db.update_kuota_request(trimmed_nomor, trimmed_kuota)
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
                    # print("masukin usernae")
                    page.fill("input[name='session[username_or_email]']", "sxtstock1")
                    # print("masukin password")
                    page.fill("input[name='session[password]']", "batiku232")
                    page.click(
                        'input[type="checkbox"]#remember'
                    )  # Selects the checkbox by ID 'remember'

                    page.click("#allow")
                    page.wait_for_selector(
                        "div.HeaderNavigationV2__style__profile"
                    )  # Replace with the correct selector for the element
