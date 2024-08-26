from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from locators import FirstPageLocators, AdvPageLocators
import pandas as pd
import re


url = 'https://www.propertyfinder.ae/en/search?l=50&c=2&fu=0&rp=y&ob=mr'


def get_adv_urls(browser, url):
    browser.get(url)
    adv_urls = browser.find_elements(*FirstPageLocators.adv)
    if adv_urls:
        for i, adv in enumerate(adv_urls):
            adv_urls[i] = adv.get_attribute('href')
    else:
        adv_urls = 'sorry, no urls found :('
    return adv_urls


def get_name(browser):
    try:
        name = browser.find_element(*AdvPageLocators.agent_name).text
    except NoSuchElementException:
        name = ':('
    return name


def get_title(browser):
    try:
        title = browser.find_element(*AdvPageLocators.adv_title).text
    except NoSuchElementException:
        title = ':('
    return title


def get_number(browser):
    try:
        whatsapp_redirect_url = browser.find_element(
            *AdvPageLocators.whatsapp_button).get_attribute('href')
        pattern = r'(\+\d+)\&'
        number = re.search(pattern, whatsapp_redirect_url).group(1)
    except NoSuchElementException:
        number = ':('
    return number


def parse_advs(browser, adv_urls):
    data = []
    for url in adv_urls:
        browser.get(url)
        browser.execute_script('window.scrollBy(0, 500);')
        name = get_name(browser)
        title = get_title(browser)
        number = get_number(browser)
        data.append([title, name, number, url])
    return data


def export(data, filename):
    columns = ['Property', 'Agent', 'Number', 'URL']
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(filename)


def main():
    try:
        browser = webdriver.Chrome()
        browser.maximize_window()

        adv_urls = get_adv_urls(browser, url)
        data = parse_advs(browser, adv_urls)
        export(data, 'arab.xlsx')  
    finally:
        browser.quit()


if __name__ == '__main__':
    main()