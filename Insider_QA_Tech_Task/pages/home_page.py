from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://useinsider.com/"

    def load(self):
        self.driver.get(self.url)

    def go_to_careers(self):
        wait = WebDriverWait(self.driver, 15)

        # Wait for the Company element to appear
        company_menu = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@class, 'nav-link') and contains(text(),'Company')]")
        ))

        # Scroll it into view just in case
        self.driver.execute_script("arguments[0].scrollIntoView(true);", company_menu)

        # Try JavaScript click instead of .click() to avoid overlay issues
        self.driver.execute_script("arguments[0].click();", company_menu)

        # Now wait and click "Careers"
        careers_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Careers']")))
        careers_link.click()