from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import db
import time
import datetime

Y = datetime.date.today().year
M = datetime.date.today().month
D = datetime.date.today().day

# clear report
# Clear report
with open(
    f"/Users/yusufkarback/ambis/selenium_basic/report{Y}{M}{D}_result_cek_kuota-1.txt",
    "w",
) as w:
    pass


def click_element(driver, locator, timeout=5):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element.click()
        return True
    except (TimeoutException, NoSuchElementException):
        print(f"Element not found or not clickable: {locator}")
        return False


def is_logged_in(driver, login_indicator_element):
    try:
        # Wait for the login indicator element to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(login_indicator_element)
        )
        print("logged in")
        return True
    except:
        return False


def get_kuota(driver):
    # Navigate to quota details
    print("Waiting to click detail kuota")
    driver.get("https://my.telkomsel.com/detail-quota/internet")

    kuota = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "QuotaDetail__style__t1"))
    )
    print("Clicked detail kuota")
    trimed_kuota = kuota.text.split()[0]
    print(trimed_kuota)
    return float(trimed_kuota)


def get_nomor(driver):
    print("getting nomor")
    nomor = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "StatusInfo__style__number"))
    )
    print(nomor)
    trimed_nomor = nomor.text.replace(" ", "")
    print(trimed_nomor)
    return trimed_nomor


with open(
    "/Users/yusufkarback/ambis/selenium_basic/account-twitter/akun-twt.txt"
) as profileLoop:
    for profile in profileLoop:
        profiles = profile.strip().split(",")
        if len(profiles) != 3:
            print(f"Invalid profile format: {profile}")
            continue

        profile_name, username, password = profiles

        if username == "#terminated" or username == "#notwitter":
            print(f"{profile_name} skipped: {username}")
            continue

        print(f"{username} Running")

        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument(
            f"--user-data-dir=/Users/yusufkarback/Library/Application\ Support/Google/Chrome"
        )
        options.add_argument(f"--profile-directory={profile_name}")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--window-position=0,0")
        options.add_argument("--window-size=1366,768")
        options.binary_location = (
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )

        try:
            service = Service(executable_path="./chromedriver")
            driver = webdriver.Chrome(service=service, options=options)
            driver.get("https://my.telkomsel.com/login/web")

            login_indicator = (By.CLASS_NAME, "HeaderNavigationV2__style__profile")

            if is_logged_in(driver, login_indicator):
                nomor = get_nomor(driver)
                kuota = get_kuota(driver)
                db.update_client_data(kuota, nomor)
            else:
                click_element(
                    driver,
                    (
                        By.XPATH,
                        "//div[contains(@class, 'PopupPromotion__style__promoButton')]//div[contains(@class, 'Button__style__neutral.Button__style__lg')]",
                    ),
                )
                # click_element(driver, (By.CLASS_NAME, "ico.icoclose"))
                print("click metode lain")

                click_element(driver, (By.CLASS_NAME, "LoginFormV2__style__socialBtn"))
                print("click login twitter")
                click_element(
                    driver,
                    (
                        By.CLASS_NAME,
                        "SocialLogin__style__socialButton.SocialLogin__style__twitter",
                    ),
                )
                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "username_or_email"))
                )
                username_field.clear()
                username_field.send_keys(username)

                password_field = driver.find_element(By.ID, "password")
                password_field.clear()
                password_field.send_keys(password)

                click_element(driver, (By.ID, "remember"))
                click_element(driver, (By.ID, "allow"))
                # driver.get("https://my.telkomsel.com/web")
                time.sleep(20)
                # get_kuota(driver)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            driver.quit()
            time.sleep(5)
