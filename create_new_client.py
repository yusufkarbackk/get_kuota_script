import json
import os
from playwright.sync_api import sync_playwright
import sys
import datetime

username = sys.argv[1]
password = sys.argv[2]

trimedPassword = password.strip("'")
trimedUsername = username.strip("'")

# TrimedSite = "dimaserang"
# trimedPassword = "batiku232"
# trimedCompany = "Bati"
# trimedUsername = "dimaserang"

profile_dir =  f"C:\\Users\\Administrator\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\profile-{trimedUsername}"

chrome_profile = f"profile-{trimedUsername}"
# Check if the directory exists, if not, create it
if not os.path.exists(profile_dir):
    os.makedirs(profile_dir)

with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            headless=False,
            executable_path="C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            user_data_dir=profile_dir,
            args=["--disable-notifications"],
            slow_mo=5000
        )
        page = browser.new_page()
        page.goto("https://my.telkomsel.com/login/web")

        profile_div = page.locator("div.HeaderNavigationV2__style__profile")
        try:
            if profile_div.is_visible():
                # print("already logged in: halaman detail kuota")
                page.goto("https://my.telkomsel.com/detail-quota/internet")
                span_text = page.text_content("span.QuotaDetail__style__t1")
                trimmed_text = span_text.split()[0]
                page.close()
                browser.close()
                data = {
                    "quota": float(trimmed_text),
                    "chrome_profile": chrome_profile,
                    "profile_path": profile_dir,
                }
                print(json.dumps(data))
                sys.stdout.flush()
            else:
                # time.sleep(120)
                # print("not logged in")

                page.click("div.DialogInstallPWADesktop__style__closeIcon")

                try:
                    page.click('text="Lanjut via website"')
                except:
                    pass            
                page.click('text="Masuk dengan metode lain"')
                page.click('text="Masuk Dengan Twitter"')

                page.click("#allow")
                try:
                    page.click("#allow")
                except:
                    pass

                page.locator('input[name="text"]').fill(trimedUsername)
                page.click('text="Next"')
                page.locator('input[name="password"]').fill(trimedPassword)
                page.click('text="Log in"')

                page.wait_for_load_state("networkidle")
                page.wait_for_selector("div.HeaderNavigationV2__style__profile", state='visible', timeout=300000)

                page.goto("https://my.telkomsel.com/detail-quota/internet")
                quota = page.text_content("span.QuotaDetail__style__t1")
                trimmed_quota = quota.split()[0]
              
                with open(
                    "C:\\xampp\\htdocs\\get_kuota_script\\new_akun_twt.txt", "a"
                ) as file:
                    file.write(f"""{chrome_profile},{trimedUsername},{trimedPassword}\n""")
                sukses = True

                browser.close()
                data = {
                    "quota": float(trimmed_quota),
                    "chrome_profile": chrome_profile,
                    "profile_path": profile_dir,
                }
                print(json.dumps(data))
                sys.stdout.flush()
        except Exception as e:
            page.close()
            browser.close()
            with open(
                    "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
            ) as file:
                file.write(f"create client {datetime.datetime.now()} {trimedUsername} error: {e}\n")
        


