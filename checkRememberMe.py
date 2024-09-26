from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

driver = webdriver.Chrome(service=service, options=options)

def checkRememberMe():
    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "username_or_email"))
                    ).clear()

                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "username_or_email"))
                    ).send_keys("dimaserang")

                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "password"))
                    ).clear()

                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "password"))
                    ).send_keys("batiku232")

                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located(
                            (
                                By.ID,
                                "remember",
                            )
                        )
                    ).click()

                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located(
                            (
                                By.ID,
                                "allow",
                            )
                        )
                    ).click()