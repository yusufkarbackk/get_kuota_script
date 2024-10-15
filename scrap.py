import json
import os
from playwright.sync_api import sync_playwright
import sys
import db
import datetime
import time

Y = datetime.date.today().year
M = datetime.date.today().month
D = datetime.date.today().day


with open("C:\\xampp\\htdocs\\get_kuota_script\\new_akun_twt.txt") as profiles:
    for profile in profiles:
        profiles = profile.strip().split(",")
        if len(profiles) != 3:
            print(f"Invalid profile format: {profile}")
            continue

        profile_name, username, password = profiles
        # print(profile_name)
        # print(username)
        # print(password)
        profile_dir = f"C:\\Users\\Administrator\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\{profile_name}"
        # Check if the directory exists, if not, create it
        if not os.path.exists(profile_dir):
            # print("create new profile")
            os.makedirs(profile_dir)
        
        with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    headless=False,
                    executable_path="C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
                    user_data_dir=profile_dir,
                    args=["--disable-notifications"],
                    slow_mo=1000

                )
                page = browser.new_page()
                page.goto("https://my.telkomsel.com/login/web")

                profile_div = page.locator("div.HeaderNavigationV2__style__profile")
                if profile_div.is_visible():
                    # print("already logged in: halaman detail kuota")
                    nomor = page.text_content("span.StatusInfo__style__number")

                    page.goto("https://my.telkomsel.com/detail-quota/internet")
                    #time.sleep(300)
                    kuota = page.text_content("span.QuotaDetail__style__t1")
                    trimmed_kuota = kuota.split()[0]
                    #trimmed_nomor = nomor.replace(" ", "")
                    print(username)
                    print(float(trimmed_kuota))
                    db.update_kuota_request(username, float(trimmed_kuota))
                    # print("sukses true")
                    page.close()
                    browser.close()
                else:
                    # time.sleep(120)
                    # print("not logged in")

                    page.click("div.DialogInstallPWADesktop__style__closeIcon")
                    try:

                        page.click('text="Lanjutkan di Web"')
                    except:
                        print("no popup")

                    try:
                        page.click('text="Masuk dengan metode lain"')
                    except:
                        print('no masuk dengan metode lain button')
                        browser.close()
                        with open(
                        "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
                        ) as file:
                                file.write(f"{profile_name}: error no masuk dengan metode lain button\n")
                        continue
                    try:
                        page.click('text="Masuk Dengan Twitter"')
                    except:
                        print('no masuk dengan twitter button')    
                    #click tombol sign in
                    page.click("#allow")
                    page.click("#allow")

                    try:
                        #twiter part
                        page.locator('input[name="text"]').fill(username)
                        page.click('text="Next"')
                        page.locator('input[name="password"]').fill(password)
                        page.click('text="Log in"')
                    except:
                        print('no enter username and password in twitter')

                    #mytelkomsel part
                    page.wait_for_load_state("networkidle")
                    page.wait_for_selector("div.HeaderNavigationV2__style__profile", state='visible', timeout=500000)

                    page.goto("https://my.telkomsel.com/detail-quota/internet")
                    span_text = page.text_content("span.QuotaDetail__style__t1")
                    trimmed_text = span_text.split()[0]
                    print(username)
                    print(float(trimmed_text))
                    db.update_kuota_request(username, float(trimmed_text))

                    #print("sukses true")
                    page.close()
                    browser.close()