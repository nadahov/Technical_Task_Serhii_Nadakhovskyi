# tests/test_career_page.py

import pytest
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.jobs_page import JobsPage

@pytest.mark.parametrize("driver", ["chrome", "firefox"], indirect=True)
def test_insider_career_page(driver):
    home = HomePage(driver)
    home.load()

    home.go_to_careers()

    careers = CareersPage(driver)
    careers.validate_sections_present()

    careers.go_to_qa_jobs()

    jobs = JobsPage(driver)
    jobs.filter_jobs()
    jobs.validate_jobs()
    jobs.check_view_role_redirect()