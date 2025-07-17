import re
import pytest
import requests
from playwright.sync_api import Browser, expect


@pytest.fixture(scope="function")
def clear_database():
    requests.delete("http://localhost:8080/users")
    yield


def test_create_user(browser: Browser, clear_database) -> None:
    page = browser.new_page(viewport=None, no_viewport=True)
    page.goto("http://localhost:5173/")

    expect(page.get_by_role("heading", name="No users found")).to_be_visible()

    page.get_by_role("button", name="Add User").click()
    page.get_by_role("textbox", name="Enter full name").click()
    page.get_by_role("textbox", name="Enter full name").fill("Vemund Santi")

    page.get_by_role("textbox", name="Enter email address").click()
    page.get_by_role("textbox", name="Enter email address").fill("vemund@santi.no")

    page.locator("form").filter(has_text="Full Name *Email Address *Add").get_by_role(
        "button"
    ).click()

    expect(
        page.locator("div")
        .filter(has_text=re.compile(r"^VSVemund Santivemund@santi\.no"))
        .first
    ).to_have_count(1)
