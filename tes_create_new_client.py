import json
import os
from playwright.sync_api import sync_playwright
import sys
import datetime

site = sys.argv[1]
password = sys.argv[2]
company = sys.argv[3]
username = sys.argv[4]

TrimedSite = site.strip("'")
trimedPassword = password.strip("'")
trimedCompany = company.strip("'")
trimedUsername = username.strip("'")

# TrimedSite = "dimaserang"
# trimedPassword = "batiku232"
# trimedCompany = "Bati"
# trimedUsername = "dimaserang"

profile_dir =  f"C:\\Users\\Administrator\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\profile-{TrimedSite}"

chrome_profile = f"profile-{TrimedSite}"
# Check if the directory exists, if not, create it
if not os.path.exists(profile_dir):
    os.makedirs(profile_dir)
data = {
    "quota": 0.0,
    "chrome_profile": chrome_profile,
    "profile_path": profile_dir,
}
print(json.dumps(data))
sys.stdout.flush()