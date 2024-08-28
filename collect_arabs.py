from selenium import webdriver
import argparse
from selenium.common.exceptions import NoSuchElementException, WebDriverException, InvalidArgumentException
from locators import FirstPageLocators, AdvPageLocators
import pandas as pd
from tqdm import tqdm
import re


BASE_URL = 'https://www.propertyfinder.ae/en/search?l=50&c=2&fu=0&rp=y&ob=mr'

parser = argparse.ArgumentParser()
parser.add_argument('--pages', type=int, default=1, required=False)
parser.add_argument('--url', type=str, default=BASE_URL, required=False)
args = parser.parse_args()


# собрать ссылки на страницы с обьявлениями в соответствии с аргументами из флагов
def get_pages():
    pages = []

    match = re.search(r'\d+$', args.url)
    if match:
        start_page = int(match.group())
    else:
        start_page = 1

    for page in range(start_page, start_page+args.pages):
        new_url = BASE_URL + f'&page={page}'
        pages.append(new_url)
    return pages


# собрать обьявления как веб-элементы и преобразовать в ссылки на обьявления
def get_adversitements_urls(browser, pages):
    collected_urls = []
    try:
        for page in pages:
            browser.get(page)
            adversitements = browser.find_elements(*FirstPageLocators.adversitement)

            urls = get_url_from_object(adversitements)
            collected_urls.extend(urls)
    except (NoSuchElementException, WebDriverException, InvalidArgumentException):
        print('что-то пошло не так :( пожалуйста, проверь ссылку или локаторы')
    finally:
        return collected_urls


# получить ссылки на обьвления из веб элементов
def get_url_from_object(adversitements):
    if adversitements:
        for i, adversitement in enumerate(adversitements):
            adversitements[i] = adversitement.get_attribute('href')
    return adversitements


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
        number = re.search(r'(\+\d+)\&', whatsapp_redirect_url).group(1)
    except NoSuchElementException:
        number = ':('
    return number


# собрать данные из каждого обьявления
def parse_adversitements(browser, adversitement_urls):
    data = []
    if adversitement_urls:
        try:
            for url in tqdm(adversitement_urls, desc="Обработано обьявлений: "):
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

        pages = get_pages()
        adversitement_urls = get_adversitements_urls(browser, pages)
        data = parse_adversitements(browser, adversitement_urls)
    finally:
        export(data, 'arab.xlsx')
        browser.quit()


if __name__ == '__main__':
    main()
