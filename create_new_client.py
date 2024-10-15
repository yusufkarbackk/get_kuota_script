import json
import os
from playwright.sync_api import sync_playwright
import sys


site = sys.argv[1]
password = sys.argv[2]
company = sys.argv[3]
username = sys.argv[4]
# with open(
#                 "C:\\xampp\\htdocs\\get_kuota_script\\error_report.txt", "a"
#             ) as file:
#                 file.write(f"{site},{password},{company}, {username}\n")
TrimedSite = site.strip("'")
trimedPassword = password.strip("'")
trimedCompany = company.strip("'")
trimedUsername = username.strip("'")

# TrimedSite = "jyskcileungsi"
# trimedPassword = "batiku232"
# trimedCompany = "Bati"
# trimedUsername = "jyskcileungsi01"

profile_dir =  f"C:\\Users\\Administrator\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\profile-{TrimedSite}"

chrome_profile = f"profile-{TrimedSite}"
# Check if the directory exists, if not, create it

if not os.path.exists(profile_dir):
    # print("create new profile")
    os.makedirs(profile_dir)
sukses = False
while sukses == False:

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            headless=False,
            executable_path="C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            user_data_dir=profile_dir,
            args=["--disable-notifications"],
            slow_mo=1500
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
            # with open(
            #     "C:\\xampp\\htdocs\\get_kuota_script\\new_akun_twt.txt", "a"
            # ) as file:
            #     file.write(f"{chrome_profile},{trimedUsername},{trimedPassword}\n")
            sukses = True
            # print("sukses true")
            browser.close()
        else:
            # time.sleep(120)
            # print("not logged in")

            page.click("div.DialogInstallPWADesktop__style__closeIcon")

            page.click('text="Lanjutkan di Web"')
            page.click('text="Masuk dengan metode lain"')
            page.click('text="Masuk Dengan Twitter"')

            page.click("#allow")
            page.click("#allow")

            page.locator('input[name="text"]').fill(trimedUsername)
            page.click('text="Next"')
            page.locator('input[name="password"]').fill(trimedPassword)
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
                file.write(f"{chrome_profile},{trimedUsername},{trimedPassword}\n")
            sukses = True
            #print("sukses true")
            browser.close()

data = {
    "quota": float(trimmed_quota),
    "phoneNumber":trimmedPhoneNumber,
    "chrome_profile": chrome_profile,
    "profile_path": profile_dir,
}
print(json.dumps(data))
sys.stdout.flush()
