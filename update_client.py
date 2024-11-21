import json
import os
from playwright.sync_api import sync_playwright
import sys
import datetime
import time

username = sys.argv[1]
password = sys.argv[2]

# trimedPassword = password.replace(" ", "")
# trimedUsername = username.replace(" ", "")

trimedPassword = password.replace(" ", "")
trimedUsername = username.replace(" ", "")

with open(
        "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
    ) as file:
    file.write(f"{username} {password}\n")

profile_dir =  f"C:\\Users\\Administrator\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\profile-{trimedUsername}"

chrome_profile = f"profile-{trimedUsername}"
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
        page.wait_for_load_state("networkidle")
        
        gagal_muat_data_element = page.locator(".QuotaDetail__style__t1")
        account_safe_element = page.locator("text='Help us keep your account safe.'")
        gagal_masuk_dengan_akun_sosial = page.locator("div.DialogSocialLoginError__style__title", has_text="Gagal Masuk dengan Akun Sosial")
        authorize_mytelkomsel_element = page.locator("h2", has_text="Authorize MyTelkomsel App to access your account?")
        profile_div = page.locator("div.HeaderNavigationV2__style__profile")
        
        try:
            if profile_div.is_visible(): #logged in
                page.goto("https://my.telkomsel.com/detail-quota/internet")
                span_text = page.text_content("span.QuotaDetail__style__t1")
                trimmed_text = span_text.split()[0]
                page.close()
                browser.close()
                data = {
                    'status' : 'success',
                    'quota' : float(trimmed_text)
                }
                print(json.dumps(data))
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

                try: # logged in but twitter sesion runs out
                    page.goto("https://my.telkomsel.com/detail-quota/internet")
                    page.wait_for_load_state("networkidle")

                    quota = page.text_content("span.QuotaDetail__style__t1")
                    trimmed_quota = quota.split()[0]

                    page.close()
                    browser.close()
                    
                    data = {
                        'status' : 'success',
                        'quota' : float(trimmed_quota)
                    }
                    print(json.dumps(data))
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
                    
                    # CEK TWEET ACCOUNT SAFE
                    if account_safe_element.is_visible():
                        data = {
                            "status" : "failed",
                            "message" : "Twitter safe account"
                        }
                        
                        print(json.dumps(data))
                        sys.stdout.flush()
                        page.close()
                        browser.close()
                    elif gagal_muat_data_element.is_visible():
                        data = {
                            "status" : "failed",
                            "message" : "Halaman Gagal Memuat Data"
                        }
                        print(json.dumps(data))
                        sys.stdout.flush()
                        page.close()
                        browser.close()
                    elif authorize_mytelkomsel_element.is_visible():
                        data = {
                            "status" : "failed",
                            "message" : "error authorize mytelkomsel app"
                        }
                        print(json.dumps(data))
                        sys.stdout.flush()
                        page.close()
                        browser.close()
                    else:
                        page.wait_for_load_state("networkidle")
                        # page.wait_for_selector("div.HeaderNavigationV2__style__profile", state='visible', timeout=300000)

                        page.goto("https://my.telkomsel.com/detail-quota/internet")
                        page.wait_for_load_state("networkidle")

                        try:
                            if gagal_muat_data_element.is_visible():
                                data = {
                                "status" : "failed",
                                "message" : "Web MyTelkomsel gagal memuat data"
                                }
                                print(json.dumps(data))
                                sys.stdout.flush()
                                page.close()
                                browser.close() 
                        except:
                            page.wait_for_load_state("networkidle")

                            quota = page.text_content("span.QuotaDetail__style__t1")
                            trimmed_quota = quota.split()[0]
                        
                            page.close()
                            browser.close()
                            
                            data = {
                                'status' : 'success',
                                'quota' : float(trimmed_quota)
                            }
                            print(json.dumps(data))
                            sys.stdout.flush()
                            page.close()
                            browser.close()
                    
        except Exception as e:
            data = {
                "status" : "failed",
                "message" : f"{e}"
                }
            print(json.dumps(data))
            sys.stdout.flush()
            page.close()
            browser.close()
            with open(
                    "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
            ) as file:
                file.write(f"update client {datetime.datetime.now()} {username} error: {e}\n")
        
