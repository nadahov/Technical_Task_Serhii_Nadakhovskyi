import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

class JobsPage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_job_cards_to_load(self):
        print("Waiting for job listings to be fully loaded...")
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.position-list-item-wrapper")))
        print("Job listings loaded.")

    def retry_click_dropdown_and_wait_for_option(self, dropdown_id, option_text, max_attempts=3):
        wait = WebDriverWait(self.driver, 15)
        attempt = 0
        option_clicked = False

        while attempt < max_attempts and not option_clicked:
            print(f"Waiting for option '{option_text}' (attempt {attempt + 1})...")
            try:
                dropdown = wait.until(EC.element_to_be_clickable((By.ID, dropdown_id)))
                dropdown.click()
                time.sleep(1)

                option_xpath = f"//li[contains(@class, 'select2-results__option') and contains(text(), '{option_text}')]"
                option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
                option.click()
                print(f"Clicked option: {option_text}")
                option_clicked = True
            except (TimeoutException, StaleElementReferenceException, ElementClickInterceptedException):
                print(f"Retrying dropdown due to missing or stale '{option_text}'...")
                attempt += 1
                time.sleep(1)

        if not option_clicked:
            raise Exception(f"Failed to click option '{option_text}' after {max_attempts} attempts.")

    def filter_jobs(self):
        wait = WebDriverWait(self.driver, 20)

        # Open location dropdown and select 'Istanbul'
        for attempt in range(3):
            print(f"Waiting for option 'Istanbul' (attempt {attempt + 1})...")
            try:
                location_dropdown = wait.until(
                    EC.element_to_be_clickable((By.ID, "select2-filter-by-location-container"))
                )
                location_dropdown.click()
                time.sleep(1)

                istanbul_option = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//li[contains(text(), 'Istanbul')]")
                    )
                )
                istanbul_option.click()
                print("Clicked option: Istanbul")
                break
            except Exception:
                print("Retrying dropdown due to missing or stale 'Istanbul'...")
                time.sleep(2)
        else:
            raise Exception("Failed to select 'Istanbul' from location filter")

        # Open department dropdown and select 'Quality Assurance'
        department_dropdown = wait.until(
            EC.element_to_be_clickable((By.ID, "select2-filter-by-department-container"))
        )
        department_dropdown.click()
        time.sleep(1)

        qa_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Quality Assurance')]"))
        )
        qa_option.click()
        print("Clicked option: Quality Assurance")

        # Force job cards rendering via slow scroll
        print("Scrolling slowly to trigger job list rendering...")
        for _ in range(10):
            self.driver.execute_script("window.scrollBy(0, 150);")
            time.sleep(0.5)

    def validate_jobs(self):
        wait = WebDriverWait(self.driver, 15)

        print("Scrolling slowly to ensure all jobs are loaded...")
        for _ in range(10):
            self.driver.execute_script("window.scrollBy(0, 150);")
            time.sleep(0.3)

        # Wait until job cards are present and at least one has non-empty text
        def job_cards_have_content(driver):
            cards = driver.find_elements(By.CSS_SELECTOR, "div.position-list-item-wrapper")
            return any(card.text.strip() for card in cards)

        try:
            wait.until(job_cards_have_content)
        except TimeoutException:
            raise AssertionError("Job cards failed to load content")

        job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.position-list-item-wrapper")
        assert job_cards, "No job cards found!"

        found = False
        for card in job_cards:
            text = card.text.lower().strip()
            print("JOB CARD TEXT:", text)
            if "quality assurance" in text:
                found = True

        assert found, "Missing 'Quality Assurance' in all job cards"

    def check_view_role_redirect(self):
        wait = WebDriverWait(self.driver, 15)
        try:
            card = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.position-list-item-wrapper"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
            time.sleep(1)

            ActionChains(self.driver).move_to_element(card).perform()
            view_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'View Role')]"))
            )

            original_window = self.driver.current_window_handle
            view_button.click()

            # Wait and switch to new tab if opened
            wait.until(lambda d: len(d.window_handles) > 1)
            for handle in self.driver.window_handles:
                if handle != original_window:
                    self.driver.switch_to.window(handle)
                    break

            wait.until(EC.url_contains("lever.co"))

        except Exception as e:
            self.driver.save_screenshot("view_role_error.png")
            raise Exception("Failed to locate or click 'View Role' button") from e