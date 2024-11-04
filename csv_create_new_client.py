import csv
import json
import os
import sys
from playwright.sync_api import sync_playwright
import db
import datetime

csv_path = sys.argv[1]

#tes_csv_path = "C:\\xampp\\htdocs\\kuota_dashboard\\writable\\uploads\\1729147529_14e544153ee6f660a890.csv"
error_string = ""
# Open the CSV file
with open(csv_path, mode='r') as file:
    csv_reader = csv.reader(file)
    
    # Skip the header (optional)
    next(csv_reader)
    
    seen = set()
    
    # Iterate through each row in the CSV
    for row in csv_reader:
        trimedSite = row[1].replace(" ", "")
        profile_dir =  f"C:\\Users\\Administrator\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\profile-{trimedSite}"

        chrome_profile = f"profile-{trimedSite}"
        # Check if the directory exists, if not, create it
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)

        with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    headless=False,
                    executable_path="C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
                    user_data_dir=profile_dir,
                    args=["--disable-notifications"],
                    slow_mo=3000
                )
                page = browser.new_page()
                page.goto("https://my.telkomsel.com/login/web")

                try:
                    page.click("div.DialogInstallPWADesktop__style__closeIcon")
                    try:
                        page.click('text="Lanjutkan di Web"')
                    except:
                        pass
                    page.click('text="Masuk dengan metode lain"')
                    page.click('text="Masuk Dengan Twitter"')

                    page.click("#allow")
                    page.click("#allow")

                    page.locator('input[name="text"]').fill(row[4])
                    page.click('text="Next"')
                    
                    page.locator('input[name="password"]').fill(row[5])
                    page.click('text="Log in"')

                        
                    page.wait_for_load_state("networkidle")
                    page.wait_for_selector("div.HeaderNavigationV2__style__profile", state='visible', timeout=300000)
                    phoneNumber = page.text_content("span.StatusInfo__style__number")
                    trimmedPhoneNumber = phoneNumber.replace(" ", "")

                    page.goto("https://my.telkomsel.com/detail-quota/internet")
                    quota = page.text_content("span.QuotaDetail__style__t1")
                    trimmed_quota = quota.split()[0]
                                # print(trimmed_quota)
                                # print(trimmedPhoneNumber) 
                    with open(
                        "C:\\xampp\\htdocs\\get_kuota_script\\new_akun_twt.txt", "a"
                    ) as file:
                        file.write(f"{chrome_profile},{row[4]},{row[5]}\n")
                                #print("sukses true")
                    browser.close()
                    
                    db.insert_new_client(row[4], trimmed_quota, trimmedPhoneNumber, profile_dir, row[2], row[1], chrome_profile)
                except:
                    page.close()
                    browser.close()
                    with open(
                        "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
                    ) as file:
                        file.write(f"CSV create client {datetime.datetime.now()}{ trimedSite} error\n")
                    error_string += f"{datetime.datetime.now()}:{trimedSite} \n"
                    continue
    print(error_string)
       