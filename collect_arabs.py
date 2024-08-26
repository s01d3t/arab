from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException, InvalidArgumentException
from locators import FirstPageLocators, AdvPageLocators
import pandas as pd
import re


BASE_URL = 'https://www.propertyfinder.ae/en/search?l=50&c=2&fu=0&rp=y&ob=mr'


def get_adversitement_urls(browser, url):
    try:
        browser.get(url)
        adversitement_urls = browser.find_elements(*FirstPageLocators.adversitement)
        if adversitement_urls:
            for i, adversitement in enumerate(adversitement_urls):
                adversitement_urls[i] = adversitement.get_attribute('href')
        else:
            print('ссылки на обьявления не найдены!')
        return adversitement_urls
    except (NoSuchElementException, WebDriverException, InvalidArgumentException):
        print('что-то пошло не так :( пожалуйста, проверь ссылку или локаторы')


def get_name(browser):
    try:
        name = browser.find_element(*AdvPageLocators.agent_name).text
    except NoSuchElementException:
        name = ':('
    return name


def get_title(browser):
    try:
        title = browser.find_element(*AdvPageLocators.adversitement_title).text
    except NoSuchElementException:
        title = ':('
    return title


def get_number(browser):
    try:
        whatsapp_redirect_url = browser.find_element(*AdvPageLocators.whatsapp_button).get_attribute('href')
        pattern = r'(\+\d+)\&'
        number = re.search(pattern, whatsapp_redirect_url).group(1)
    except NoSuchElementException:
        number = ':('
    return number


def parse_advs(browser, adversitement_urls):
    data = []
    if adversitement_urls:
        try:
            for url in adversitement_urls:
                browser.get(url)
                browser.execute_script('window.scrollBy(0, 500);')
                name = get_name(browser)
                title = get_title(browser)
                number = get_number(browser)
                data.append([title, name, number, url])
        finally:
            return data
   

def export(data, filename):
    if data:
        columns = ['Property', 'Agent', 'Number', 'URL']
        df = pd.DataFrame(data, columns=columns)
        df.to_excel(filename)
    else:
        print('нечего экспортировать :(')


def main():
    try:
        browser = webdriver.Chrome()
        browser.maximize_window()

        adversitement_urls = get_adversitement_urls(browser, BASE_URL)
        data = parse_advs(browser, adversitement_urls)
    finally:
        export(data, 'arab.xlsx')
        browser.quit()


if __name__ == '__main__':
    main()