import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import modules.auth
import random 
import itertools

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)

# driver.get("https://www.tripadvisor.ru/")
# modules.auth.auth(driver)

url_query = [
    'https://www.tripadvisor.ru/Attraction_Review-g298491-d300053-Reviews-Kamchatka_Peninsula-Kamchatka_Krai_Far_Eastern_District.html',
    'https://www.tripadvisor.ru/Attraction_Review-g17182817-d10859495-Reviews-Primorsky_Aquarim-Russkiy_Primorsky_Krai_Far_Eastern_District.html',
    'https://www.tripadvisor.ru/Attraction_Review-g298496-d600367-Reviews-S_56_Submarine_Museum-Vladivostok_Primorsky_Krai_Far_Eastern_District.html',
    'https://www.tripadvisor.ru/Attraction_Review-g298497-d300136-Reviews-Gagarin_Park-Yuzhno_Sakhalinsk_Sakhalin_Sakhalin_Oblast_Far_Eastern_District.html',
    'https://www.tripadvisor.ru/Attraction_Review-g298493-d4743933-Reviews-Spaso_Transfiguration_Cathedral-Khabarovsk_Khabarovsk_Krai_Far_Eastern_District.html',
    'https://www.tripadvisor.ru/Attraction_Review-g665309-d4555683-Reviews-Lenskiy_Pillars-Yakutsk_Sakha_Yakutia_Republic_Far_Eastern_District.html',
    'https://www.tripadvisor.ru/Attraction_Review-g298496-d6491469-Reviews-Voroshilovskaya_Batareya_Museum-Vladivostok_Primorsky_Krai_Far_Eastern_District.html',
]

for url in url_query:
    # url = "https://www.tripadvisor.ru/Attraction_Review-g298496-d308059-Reviews-Svetlanskaya_Street-Vladivostok_Primorsky_Krai_Far_Eastern_District.html"
    time.sleep(random.randint(1, 5))
    driver.get(url)
    reviews = []

    is_two_cities = False

    att_type = ''
    att_name = ''

    try:
        page_breadcrumbs = driver.find_element(By.CSS_SELECTOR, '*[data-automation="breadcrumbs"]')
        zone = page_breadcrumbs.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > a > span > span').text
        region = page_breadcrumbs.find_element(By.CSS_SELECTOR, 'div:nth-child(4) > a > span > span').text
        city = page_breadcrumbs.find_element(By.CSS_SELECTOR, 'div:nth-child(5) > a > span > span').text

        if is_two_cities:
            city += ","
            city += page_breadcrumbs.find_element(By.CSS_SELECTOR, 'div:nth-child(6) > a > span > span').text
            att_type = page_breadcrumbs.find_element(By.CSS_SELECTOR, 'div:nth-child(7) > a > span > span').text
            att_name = page_breadcrumbs.find_element(By.CSS_SELECTOR, 'div:nth-child(8) > span > span').text
        else:
            att_type = page_breadcrumbs.find_element(By.CSS_SELECTOR, 'div:nth-child(6) > a > span > span').text
            att_name = page_breadcrumbs.find_element(By.CSS_SELECTOR, 'div:nth-child(7) > span > span').text
    except Exception:
        print("bad breadcrumb")

    page_counter = 0
    while True:
        page_counter+=1
        print(f"current page is {page_counter}")
        current_reviews = driver.find_elements(By.CSS_SELECTOR, '*[data-automation="reviewCard"]')

        for review in current_reviews:
            try:
                author = review.find_element(By.CSS_SELECTOR, 'div div:nth-child(1) div:nth-child(1) div:nth-child(2) span a').text
                author_location = review.find_element(By.CSS_SELECTOR, 'div div:nth-child(1) div:nth-child(1) div:nth-child(2) > div > div > span:nth-child(1)').text
                rating = len(review.find_elements(By.CSS_SELECTOR, 'div div:nth-child(2) svg path[d="M 12 0C5.388 0 0 5.388 0 12s5.388 12 12 12 12-5.38 12-12c0-6.612-5.38-12-12-12z"]'))
                comment = review.find_element(By.CSS_SELECTOR, 'div div:nth-child(5) div:nth-child(1) div:nth-child(1) > span > span').text
                comment_date = review.find_element(By.CSS_SELECTOR, 'div > div:nth-child(7) > div:nth-child(1)').text
            except:
                print("cant find part of")
            line = [zone, region, city, att_type, att_name, author, rating, comment, comment_date]

            print(line)
            print('\n')

            reviews.append(line)
        time.sleep(random.randint(5, 15))

        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[7]/div/div/div/section/section/div[1]/div/div[5]/div/div[11]/div[1]/div/div[1]/div[2]/div/a").click()
            time.sleep(random.randint(2, 12))
        except:
            print("end of reviews list")
            break


    path_to_file = f'./files/reviews_{url[len("https://www.tripadvisor.ru/")::]}.csv'
    reviews.sort()
    reviews = list(k for k,_ in itertools.groupby(reviews))
    with open(path_to_file, 'a', encoding="utf-8") as csvfile:
        csvWriter = csv.writer(csvfile)
        for review in reviews:
            csvWriter.writerow(review)

driver.quit()
