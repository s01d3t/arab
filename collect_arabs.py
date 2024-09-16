from selenium.common.exceptions import NoSuchElementException, WebDriverException, InvalidArgumentException
from locators import FirstPageLocators, AdvPageLocators
import pandas as pd
from tqdm import tqdm
import re
from selenium import webdriver

BASE_URL = 'https://www.propertyfinder.ae/en/search?l=50&c=2&fu=0&rp=y&ob=mr'


def driver():
    browser = webdriver.Chrome()
    browser.maximize_window()
    return browser


# получить стартовую ссылку и количество страниц для обработки
def get_input():
    while True:
        input_url = input(
            'пожалуйста, укажи ссылку на страницу. оставь поле пустым, чтобы начать c первой страницы: ').strip()
        if input_url.startswith(BASE_URL):
            pass
        elif len(input_url) == 0:
            input_url = BASE_URL
        else:
            print('неправильная ссылка, попробуй снова')
            continue
        print('принято')

        input_pages = input(
            'пожалуйста, укажи количество страниц. оставь поле пустым, чтобы обработать одну страницу: ').strip()
        if input_pages.isdigit():
            pass
        elif len(input_pages) == 0:
            input_pages = 1
        else:
            print('неправильное количество страниц. попробуй снова\n')

            continue
        print('принято')

        return input_url, input_pages


# собрать ссылки на страницы с обьявлениями в соответствии с аргументами из флагов
def get_pages(input_url, input_pages=1):
    pages = []
    match = re.search(r'page=(\d+)$', input_url)
    if match:
        start_page = int(match.group(1))
    else:
        start_page = 1

    for page in range(start_page, start_page + int(input_pages)):
        new_url = BASE_URL + f'&page={page}'
        pages.append(new_url)
    return pages


# собрать обьявления как веб-элементы и преобразовать в ссылки на обьявления
def get_adversitements_urls(browser, pages):
    collected_urls = []
    for page in pages:
        try:
            browser.get(page)
            adversitements = browser.find_elements(*FirstPageLocators.adversitement)
            urls = get_url_from_object(adversitements)
            collected_urls.extend(urls)
        except (WebDriverException, InvalidArgumentException):
            print(f'эта ссылка сломана :( - [{page}]')
        except NoSuchElementException:
            print('элемент не найден :(')

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
        number = re.search(r'(\+\d+)&', whatsapp_redirect_url).group(1)
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
        with pd.ExcelWriter(filename) as writer:
            df.to_excel(writer, index=False)
    else:
        print('нечего экспортировать :(')


def main():
    try:
        input_url, input_pages = get_input()
        pages = get_pages(input_url, input_pages)
        browser = driver()
        adversitement_urls = get_adversitements_urls(browser, pages)
        data = parse_adversitements(browser, adversitement_urls)
    finally:
        export(data, 'arab.xlsx')
        browser.quit()


if __name__ == '__main__':
    main()
