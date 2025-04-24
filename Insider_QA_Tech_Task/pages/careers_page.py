from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CareersPage:
    def __init__(self, driver):
        self.driver = driver

    def validate_sections_present(self):
        wait = WebDriverWait(self.driver, 15)
        assert wait.until(EC.presence_of_element_located((By.XPATH, "//section[contains(., 'Find your calling')]")))
        assert wait.until(EC.presence_of_element_located((By.XPATH, "//section[contains(., 'Life at Insider')]")))
        assert wait.until(EC.presence_of_element_located((By.XPATH, "//section[contains(., 'Our Locations')]")))

    def go_to_qa_jobs(self):
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        wait = WebDriverWait(self.driver, 10)

        # Handle the cookie popup if present
        try:
            accept_button = wait.until(EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn")))
            accept_button.click()
        except Exception:
            pass  # If not found, continue

        # Scroll to and click the "See all QA jobs" button via JS to avoid intercept
        see_all_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[text()='See all QA jobs']")
        ))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", see_all_button)
        self.driver.execute_script("arguments[0].click();", see_all_button)