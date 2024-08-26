from selenium.webdriver.common.by import By


class FirstPageLocators():
    adversitement = (By.CLASS_NAME, 'property-card-module_property-card__link__L6AKb')


class AdvPageLocators():
    adversitement_title = (By.CLASS_NAME, 'styles_desktop_title__j0uNx')
    agent_name = (By.CLASS_NAME, 'styles_agent__name__iexLd')
    whatsapp_button = (By.CSS_SELECTOR, 'a[data-testid="bottom-actions-whatsapp-button"]')
