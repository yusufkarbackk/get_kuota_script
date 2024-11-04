import json
import os
from playwright.sync_api import sync_playwright
import sys
import datetime
import time

site = sys.argv[1]
password = sys.argv[2]
company = sys.argv[3]
username = sys.argv[4]

TrimedSite = site.strip("'")
trimedPassword = password.strip("'")
trimedCompany = company.strip("'")
trimedUsername = username.strip("'")

profile_dir =  f"C:\\Users\\Administrator\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\profile-{TrimedSite}"

chrome_profile = f"profile-{TrimedSite}"
# Check if the directory exists, if not, create it
if not os.path.exists(profile_dir):
    os.makedirs(profile_dir)

with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            headless=False,
            executable_path="C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            user_data_dir=f"{profile_dir}",
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
                # data = {
                #     "quota": float(trimmed_text),
                # }
                print(float(trimmed_text))
                sys.stdout.flush()   
            else:
                page.click("div.DialogInstallPWADesktop__style__closeIcon") 

                try:
                    page.click('text="Lanjut via website    "')
                except:
                    pass            
                page.click('text="Masuk dengan metode lain"')
                page.click('text="Masuk Dengan Twitter"')
                page.wait_for_load_state("networkidle")

                try:
                    page.goto("https://my.telkomsel.com/detail-quota/internet")
                    quota = page.text_content("span.QuotaDetail__style__t1")
                    trimmed_quota = quota.split()[0]
                        # print(trimmed_quota)
                        # print(trimmedPhoneNumber)
                    # with open(
                    #         "C:\\xampp\\htdocs\\get_kuota_script\\new_akun_twt.txt", "a"
                    # ) as file:
                    #     file.write(f"""{chrome_profile},{trimedUsername},{trimedPassword}\n""")
                    page.close()
                    browser.close()
                    
                    # data = {
                    #         "quota": float(trimmed_quota),
                    # }
                    print(float(trimmed_quota))
                    sys.stdout.flush()   

                except:
                    page.click('text="Masuk dengan metode lain"')
                    page.click('text="Masuk Dengan Twitter"')
                    page.click("#allow")
                    try:
                        page.click("#allow")
                    except:
                        pass
                    page.wait_for_load_state("networkidle")
                    page.locator('input[name="text"]').fill(trimedUsername)
                    page.click('text="Next"')
                    page.locator('input[name="password"]').fill(trimedPassword)
                    page.click('text="Log in"')

                    page.wait_for_load_state("networkidle")
                    #page.wait_for_selector("div.HeaderNavigationV2__style__profile", state='visible', timeout=300000)
                        # phoneNumber = page.text_content("span.StatusInfo__style__number")
                        # trimmedPhoneNumber = phoneNumber.replace(" ", "")

                    page.goto("https://my.telkomsel.com/detail-quota/internet")
                    quota = page.text_content("span.QuotaDetail__style__t1")
                    trimmed_quota = quota.split()[0]
                        # print(trimmed_quota)
                        # print(trimmedPhoneNumber)
                    # with open(
                    #         "C:\\xampp\\htdocs\\get_kuota_script\\new_akun_twt.txt", "a"
                    # ) as file:
                    #     file.write(f"""{chrome_profile},{trimedUsername},{trimedPassword}\n""")
                    page.close()
                    browser.close()
                    
                    # data = {
                    #         "quota": float(trimmed_quota),
                    # }
                    print(float(trimmed_quota))
                    sys.stdout.flush()
                    
        except Exception as e:
            page.close()
            browser.close()
            with open(
                    "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
            ) as file:
                file.write(f"update client {datetime.datetime.now()} {site} error: {e}\n")
        
