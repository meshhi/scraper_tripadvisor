from selenium.webdriver.common.by import By
import time

def auth(driver):
    driver.find_element(By.XPATH, '//*[@id="lithium-root"]/header/div/nav/div[3]/a').click()

    driver.find_element(By.XPATH, '/html/body/div[3]/div/div[1]/div[3]/div/div[1]/button/span[2]').click()

    time.sleep(1)

    login = driver.find_element(By.XPATH, '//*[@id="regSignIn.email"]')
    for character in "mehhi@yandex.ru":
        login.send_keys(character)
        time.sleep(0.3)

    password = driver.find_element(By.XPATH, '//*[@id="regSignIn.password"]')
    for character in "Mams228322!":
        password.send_keys(character)
        time.sleep(0.3)
    
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="regSignIn"]/div[4]/button[1]').click()
    time.sleep(1)