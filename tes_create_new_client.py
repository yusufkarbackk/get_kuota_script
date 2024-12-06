import json
import os
from playwright.sync_api import sync_playwright
import sys
import datetime
import time

from remove_folders import remove_folders

username = sys.argv[1]
password = sys.argv[2]

trimedPassword = password.replace(" ", "")
trimedUsername = username.replace(" ", "")
    
# trimedPassword = "batiku232"
# trimedUsername = "@KramatPezzo"

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
            args=["--disable-notifications", "--disable-logging"],
            slow_mo=5000
        )
        page = browser.new_page()
        page.goto("https://my.telkomsel.com/login/web")
        page.wait_for_load_state("networkidle")
        
        
        account_safe_element = page.locator("text='Help us keep your account safe.'")
        gagal_masuk_dengan_akun_sosial = page.locator("div.DialogSocialLoginError__style__title", has_text="Gagal Masuk dengan Akun Sosial")
        authorize_mytelkomsel_element = page.locator("h2", has_text="Authorize MyTelkomsel App to access your account?")
        profile_div = page.locator("div.HeaderNavigationV2__style__profile")
        
        try:
            try:
                page.click("div.DialogInstallPWADesktop__style__closeIcon") 
            except:
                pass
            try:
                page.click('text="Lanjut via website"')
            except:
                pass  
            page.click('text="Masuk dengan metode lain"')
            page.click('text="Masuk Dengan Twitter"')
            page.wait_for_load_state("networkidle")
            
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
                        #sys.stdout.flush()
                        page.close()
                        browser.close()
                        remove_folders(profile_dir)
                elif authorize_mytelkomsel_element.is_visible():
                        data = {
                            "status" : "failed",
                            "message" : "error authorize mytelkomsel app"
                        }
                        print(json.dumps(data))
                        #sys.stdout.flush()
                        page.close()
                        browser.close()
                        remove_folders(profile_dir)
                else:
                        page.wait_for_load_state("networkidle")
                        page.wait_for_selector("div.HeaderNavigationV2__style__profile", state='visible', timeout=300000)

                        page.goto("https://my.telkomsel.com/detail-quota/internet")
                        page.wait_for_load_state("networkidle")
                        page.wait_for_selector("span.QuotaDetail__style__t1", state='visible', timeout=30000)

                        if page.text_content("span.QuotaDetail__style__t1") == "Gagal Memuat Data":
                            data = {
                                "status" : "failed",
                                "message" : "Web MyTelkomsel gagal memuat data",
                                "chrome_profile" : chrome_profile
                            }
                            print(json.dumps(data))
                            sys.stdout.flush()
                            page.close()
                            browser.close() 
                            remove_folders(profile_dir)
                        else:
                            page.wait_for_load_state("networkidle")
                            page.wait_for_selector("span.QuotaDetail__style__t1", state='visible', timeout=30000)
                            span_text = page.text_content("span.QuotaDetail__style__t1")
                            trimmed_text = span_text.split()[0]
                            unit = span_text.split()[1]
                            # quota = "{:.2f}".format(float(688.81) / 1024)

                            if unit == "GB":
                                quota = float(trimmed_text)
                            elif unit == "MB":
                                quota = "{:.2f}".format(float(trimmed_text) / 1024)
                            
                            data = {
                                "status" : "success",
                                "quota" : quota,
                                "chrome_profile" : chrome_profile,
                                "profile_path" : profile_dir
                            }
                            with open(
                                "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
                            ) as file:
                                file.write(f"{data}\n")
                            
                            print(json.dumps(data))
                            #sys.stdout.flush()   
                            page.close()
                            browser.close()
                            
                            remove_folders(profile_dir)
        except Exception as e:
            data = {
                "status" : "failed",
                "message" : f"{e}"
                }
            print(json.dumps(data))
            #sys.stdout.flush()
            page.close()
            browser.close()
            remove_folders(profile_dir)

            with open(
                    "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
            ) as file:
                file.write(f"update client {datetime.datetime.now()} {trimedUsername} error: {e}\n")
         
        
        
        
        
        
        
        
        # try:
        #     page.click("div.DialogInstallPWADesktop__style__closeIcon") 

        #     try:
        #         page.click('text="Lanjut via website"')
        #     except:
        #             pass            
        #     page.click('text="Masuk dengan metode lain"')
        #     page.click('text="Masuk Dengan Twitter"')
        #     page.wait_for_load_state("networkidle")

        #     try: # logged in but twitter sesion runs out
        #         page.goto("https://my.telkomsel.com/detail-quota/internet")
        #         try:
        #                 page.wait_for_selector("span.QuotaDetail__style__t1", timeout=5000)
        #                 gagal_muat_data_element = page.locator("span.QuotaDetail__style__t1").text_content()
        #                 gagal_muat_data_element == "Gagal Memuat Data"
        #                 data = {
        #                         "status" : "failed",
        #                         "message" : "Gagal Memuat Data",
        #                 }
                            
        #                 print(json.dumps(data))
        #                 #sys.stdout.flush()   
        #                 page.close()
        #                 browser.close()                        
        #                 remove_folders(profile_dir)
                    
        #             # tidak_ada_kuota = page.locator("span.QuotaDetail__style__title").nth(5).text_content()
        #         except:
        #                 try:
        #                     page.locator("span.QuotaDetail__style__title").nth(5).text_content() == "Anda tidak memiliki kuota"
        #                     data = {
        #                         "status" : "success",
        #                         "quota" : 0.0,
        #                     }
                            
        #                     print(json.dumps(data))
        #                     #sys.stdout.flush()   
        #                     page.close()
        #                     browser.close()
                            
        #                     remove_folders(profile_dir)
        #                 except:
        #                     span_text = page.text_content("span.QuotaDetail__style__t1")
        #                     trimmed_text = span_text.split()[0]
        #                     unit = span_text.split()[1]
        #                     # quota = "{:.2f}".format(float(688.81) / 1024)

        #                     if unit == "GB":
        #                         quota = float(trimmed_text)
        #                     elif unit == "MB":
        #                         quota = "{:.2f}".format(float(trimmed_text) / 1024)
                            
        #                     data = {
        #                         "status" : "success",
        #                         "quota" : quota,
        #                         'unit' : unit
        #                     }
        #                     with open(
        #                         "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
        #                     ) as file:
        #                         file.write(f"{data}\n")
                            
        #                     print(json.dumps(data))
        #                     #sys.stdout.flush()   
        #                     page.close()
        #                     browser.close()
                            
        #                     remove_folders(profile_dir)
        #     except:
        #             page.click('text="Masuk dengan metode lain"')
        #             page.click('text="Masuk Dengan Twitter"')
        #             page.click("#allow")
        #             try:
        #                 page.click("#allow")
        #             except:
        #                 pass
        #             page.wait_for_load_state("networkidle")
        #             page.locator('input[name="text"]').fill(trimedUsername)
        #             page.click('text="Next"')
        #             page.locator('input[name="password"]').fill(trimedPassword)
        #             page.click('text="Log in"')

        #             page.wait_for_load_state("networkidle")
                    
        #             # CEK TWEET ACCOUNT SAFE
        #             if account_safe_element.is_visible():
        #                 data = {
        #                     "status" : "failed",
        #                     "message" : "Twitter safe account"
        #                 }
                        
        #                 print(json.dumps(data))
        #                 #sys.stdout.flush()
        #                 page.close()
        #                 browser.close()
        #                 remove_folders(profile_dir)
        #             elif authorize_mytelkomsel_element.is_visible():
        #                 data = {
        #                     "status" : "failed",
        #                     "message" : "error authorize mytelkomsel app"
        #                 }
        #                 print(json.dumps(data))
        #                 #sys.stdout.flush()
        #                 page.close()
        #                 browser.close()
        #                 remove_folders(profile_dir)
        #             else:
        #                 page.wait_for_load_state("networkidle")
        #                 page.wait_for_selector("div.HeaderNavigationV2__style__profile", state='visible', timeout=300000)

        #                 page.goto("https://my.telkomsel.com/detail-quota/internet")
        #                 page.wait_for_load_state("networkidle")
        #                 page.wait_for_selector("span.QuotaDetail__style__t1", state='visible', timeout=30000)

        #                 if page.text_content("span.QuotaDetail__style__t1") == "Gagal Memuat Data":
        #                     data = {
        #                         "status" : "failed",
        #                         "message" : "Web MyTelkomsel gagal memuat data"
        #                     }
        #                     print(json.dumps(data))
        #                     sys.stdout.flush()
        #                     page.close()
        #                     browser.close() 
        #                     remove_folders(profile_dir)
        #                 else:
        #                     page.wait_for_load_state("networkidle")
        #                     page.wait_for_selector("span.QuotaDetail__style__t1", state='visible', timeout=30000)
        #                     span_text = page.text_content("span.QuotaDetail__style__t1")
        #                     trimmed_text = span_text.split()[0]
        #                     unit = span_text.split()[1]
        #                     # quota = "{:.2f}".format(float(688.81) / 1024)

        #                     if unit == "GB":
        #                         quota = float(trimmed_text)
        #                     elif unit == "MB":
        #                         quota = "{:.2f}".format(float(trimmed_text) / 1024)
                            
        #                     data = {
        #                         "status" : "success",
        #                         "quota" : quota,
        #                         'unit' : unit
        #                     }
        #                     with open(
        #                         "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
        #                     ) as file:
        #                         file.write(f"{data}\n")
                            
        #                     print(json.dumps(data))
        #                     #sys.stdout.flush()   
        #                     page.close()
        #                     browser.close()
                            
        #                     remove_folders(profile_dir)
        # except TimeoutError as e:
        #     data = {
        #         "status" : "failed",
        #         "message" : "element not found"
        #     }
        #     print(json.dumps(data))
        #     sys.stdout.flush()
        #     page.close()
        #     browser.close()
        #     with open(
        #                 "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
        #     ) as file:
        #         file.write(f"create client {datetime.datetime.now()} {trimedUsername} error: element not found \n")
        # except Exception as e:
        #     data = {
        #         "status" : "failed",
        #         "message" : f"{e}"
        #         }
        #     print(json.dumps(data))
        #     #sys.stdout.flush()
        #     page.close()
        #     browser.close()
        #     remove_folders(profile_dir)

        #     with open(
        #             "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
        #     ) as file:
        #         file.write(f"update client {datetime.datetime.now()} {trimedUsername} error: {e}\n")
        
