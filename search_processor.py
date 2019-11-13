import pool
import time
from wait_any_key import wait_any_key

import config

from selenium.webdriver.support.ui import Select


def search_process():

    driver = pool.get()

    driver.get("http://www.aski.gov.tr/TR/SuAnalizSonuclari.aspx")

    driver.find_element_by_xpath("//select[@name='DDILLER']/option[text()='YENİMAHALLE']").click()

    datelist = []

    elem = driver.find_element_by_name("DDTarih")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == "Tarih Seçiniz":
            continue

        datelist.append(option.text)

    for date in datelist:
        select = Select(driver.find_element_by_id('DDTarih'))
        select.select_by_value(date)
        driver.find_element_by_name("Button1").click()

        sulfat = driver.find_element_by_xpath("//tr/td[text()='Sülfat']")
        sulfat_row = sulfat.find_element_by_xpath('..')
        values = sulfat_row.find_elements_by_tag_name("td")
        sulfat_value = values[2].text
        print("{}:{}".format(date, sulfat_value))

    wait_any_key()



    finished = False
    cur_page = 0

    while not finished:
        cur_page += 1
        driver.get("http://www.aski.gov.tr/TR/SuAnalizSonuclari.aspx")
        done_with_page = False
        while not done_with_page:
            try:
                connect_button = driver.find_element_by_xpath("//button[text()='Connect']")
                connect_button.click()
                time.sleep(2)

                try:
                    email_input = driver.find_element_by_xpath("//input[@id='email']")
                    email_input.send_keys(config.invite_email_to_send)
                    time.sleep(2)
                except:
                    pass

                try:
                    snd_now_button = driver.find_element_by_xpath("//button[text()='Send now']")
                    snd_now_button.click()
                    time.sleep(2)
                except:
                    pass

            except:
                scroll = driver.execute_script("return window.pageYOffset")
                driver.execute_script("window.scrollBy(0, 100);")

                time.sleep(2)

                if scroll == driver.execute_script("return window.pageYOffset"):
                    done_with_page = True

        time.sleep(2)
        print(driver.current_url)

    print("done")
    return
