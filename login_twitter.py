import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import db
import time

# Get the username and email passed from the PHP controller
print(sys.argv)
# client = sys.argv[1]
# password = sys.argv[2]
# number = sys.argv[3]
# chrome_profile = sys.argv[4]
# company = sys.argv[5]
# team_flag = sys.argv[6]

client = "sxtstock1"
password = "batiku232"
number = "081119026097"
chrome_profile = "40"
company = "sxtstock1"
team_flag = "bati"


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
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'QuotaDetail__style__quotaInfoWrapper')]//span[contains(@class, 'QuotaDetail__style__t1')]",
            )
        )
    )
    print("Clicked detail kuota")
    print(kuota.text)
    trimed_kuota = kuota.text.split()[0]
    print(trimed_kuota)
    return float(trimed_kuota)


def get_nomor(driver):
    print("getting nomor")
    nomor = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "StatusInfo__style__number"))
    )
    trimed_nomor = nomor.text.replace(" ", "")
    print(trimed_nomor)
    return trimed_nomor


print(f"{client} Running")

sukses = False

while sukses == False:
    options = Options()
    options.page_load_strategy = "normal"
    options.add_argument("--disable-notifications")
    options.add_argument(
        f"--user-data-dir=/Users/yusufkarback/Library/Application\ Support/Google/Chrome"
    )
    options.add_argument(f"--profile-directory={chrome_profile}")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--window-position=0,0")
    options.add_argument("--window-size=1366,768")
    options.binary_location = (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    )
    try:
        service = Service(
            executable_path="/Users/yusufkarback/ambis/selenium_basic/chromedriver"
        )
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://my.telkomsel.com/login/web")

        login_indicator = (By.CLASS_NAME, "HeaderNavigationV2__style__profile")

        if is_logged_in(driver, login_indicator):
            nomor = get_nomor(driver)
            kuota = get_kuota(driver)
            db.insert_client(
                client,
                company,
                team_flag,
                nomor,
                kuota,
                chrome_profile,
                "/Users/yusufkarback/Library/Application\ Support/Google/Chrome",
            )
            sukses = True
            # db.insert_history_data(nomor)
        else:
            try:

                close_icon = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//div[@data-testid='bottomSheetClose']//i[contains(@class, 'ico') and contains(@class, 'icoClose') and contains(@class, 'BottomSheet_style_closeIcon')]",
                        )
                    )
                )
                close_icon.click()

            # click_element(
            #     driver,
            #     (
            #         By.CSS_SELECTOR,
            #         "button.Button_style_neutral__Button_style_lg[data-testid='button']",
            #     ),
            # )
            except:
                print("Pop-up not found or already closed")

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
            username_field.send_keys(client)

            password_field = driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(password)

            click_element(driver, (By.ID, "remember"))
            click_element(driver, (By.ID, "allow"))
            # driver.get("https://my.telkomsel.com/web")
            time.sleep(20)
            # get_kuota(driver)
            driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")
        webdriver.Chrome().quit()
# driver.quit()
# Write the data to a text file
with open("/Users/yusufkarback/ambis/selenium_basic/new_akun_twt.txt", "a") as file:
    file.write(f"profile{int(chrome_profile)+1},{client},{password}\n")

print(f"User {client} created successfully!")
