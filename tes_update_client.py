import json
import os
from playwright.async_api import async_playwright
import sys
import datetime
import asyncio

import time

async def process_profile(profile):
    trimedPassword = profile['password'].replace(" ", "")
    trimedUsername = profile['username'].replace(" ", "")
    profile_dir =  f"C:\\Users\\Administrator\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\profile-{trimedUsername}"

    result = []
    
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)

    try:
        async with async_playwright() as p:
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
            # gagal_masuk_dengan_akun_sosial = page.locator("div.DialogSocialLoginError__style__title", has_text="Gagal Masuk dengan Akun Sosial")
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
                        'quota' : float(trimmed_text),
                        'account_id' : profile['id']
                    }
                    return result.append(json.dumps(data))
                    # print(json.dumps(data))
                    # sys.stdout.flush()   
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
                            'quota' : float(trimmed_quota),
                            'account_id' : profile['id']
                        }
                        return result.append(json.dumps(data))
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
                                "message" : "Twitter safe account",
                                'account_id' : profile['id']
                            }
                            page.close()
                            browser.close()
                            return result.append(json.dumps(data))

                            # print(json.dumps(data))
                            # sys.stdout.flush()
                            
                        elif gagal_muat_data_element.is_visible():
                            data = {
                                "status" : "failed",
                                "message" : "Halaman Gagal Memuat Data",
                                'account_id' : profile['id']
                            }
                            page.close()
                            browser.close()
                            return result.append(json.dumps(data))
                            # print(json.dumps(data))
                            # sys.stdout.flush()
                            
                        elif authorize_mytelkomsel_element.is_visible():
                            data = {
                                "status" : "failed",
                                "message" : "error authorize mytelkomsel app",
                                "account_id" : profile['id']
                            }
                            page.close()
                            browser.close()
                            return result.append(json.dumps(data))
                            # print(json.dumps(data))
                            # sys.stdout.flush()
                            
                        else:
                            page.wait_for_load_state("networkidle")
                            # page.wait_for_selector("div.HeaderNavigationV2__style__profile", state='visible', timeout=300000)

                            page.goto("https://my.telkomsel.com/detail-quota/internet")
                            page.wait_for_load_state("networkidle")

                            try:
                                if gagal_muat_data_element.is_visible():
                                    data = {
                                    "status" : "failed",
                                    "message" : "Web MyTelkomsel gagal memuat data",
                                    'account_id' : profile['id']
                                    }
                                    result.append(json.dumps(data))

                                    # print(json.dumps(data))
                                    # sys.stdout.flush()
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
                                    'quota' : float(trimmed_quota),
                                    'account_id' : profile['id']
                                }
                                result.append(json.dumps(data))
                                # print(json.dumps(data))
                                # sys.stdout.flush()
                                page.close()
                                browser.close()       
            except Exception as e:
                data = {
                    "status" : "failed",
                    "message" : f"{e}",
                    'account_id' : profile['id']
                    }
                result.append(json.dumps(data))
                # print(json.dumps(data))
                # sys.stdout.flush()
                page.close()
                browser.close()
                with open(
                        "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
                ) as file:
                    file.write(f"update client {datetime.datetime.now()} {profile['username']} error: {e}\n")

    except Exception as e:
        with open(
                        "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
                ) as file:
                    file.write(f"{e}\n")
async def main():
    # TrimedSite = "tes_site"
    # trimedPassword = "batiku"
    # trimedCompany = "tes_company"   
    # trimedUsername = "tes_username"
        
    try:
        profiles = json.loads(sys.argv[1])
        results = await asyncio.gather(*(process_profile(profile) for profile in profiles)) 
        print(json.dumps(results))
    except Exception as e:
         with open(
                        "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
                ) as file:
                    file.write(f"{e}\n {profiles}")


if __name__ == "__main__":
    asyncio.run(main())
# chrome_profile = f"profile-{TrimedSite}"
# Check if the directory exists, if not, create it

