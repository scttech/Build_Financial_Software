from pathlib import Path
from random import randint

import pytest
from playwright.sync_api import Page, expect, sync_playwright

from chapter10.v4.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter10.v4.AchParser.tests.ach_processor.sql_utils import SqlUtils

# Get the directory of our script
current_file_dir = Path(__file__).resolve().parent


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    pages = context.pages
    page = pages[0] if pages else context.new_page()
    yield page
    context.close()


@pytest.fixture(autouse=True)
def setup_teardown_method():
    # Clear the database
    SqlUtils.truncate_all()

    # Load a file into the database
    ach_file = "./data/sally_saver.ach"
    file_path = get_absolute_path("./data/sally_saver.ach")
    parser = AchFileProcessor()
    ach_files_id = SqlUtils.create_ach_file_record(ach_file, str(randint(1, 99999999)))
    parser.parse(ach_files_id, file_path)
    yield


def get_absolute_path(relative_path):
    return current_file_dir / relative_path


@pytest.mark.page
def test_dashboard(page: Page):
    # Navigate to the search page and perform a search
    page.goto("http://localhost:3000/search")
    page.expect_navigation(wait_until="load")
    expect(page).to_have_url("http://localhost:3000/search")
    search_criteria = page.get_by_role("textbox")
    search_criteria.fill("sally saver")
    search_button = page.locator("#searchbtn")
    with page.expect_response("**/files/transactions/search*") as response_info:
        search_button.click()

    response = response_info.value
    assert response.status == 200
    search_result = page.locator('div[title="Sally Saver"]')
    expect(search_result).to_be_visible()
    page.screenshot(path="screenshots/search_results.png")
