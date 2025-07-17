import re
import pytest
import requests
from playwright.sync_api import Browser, expect


@pytest.fixture(scope="function")
def clear_database():
    requests.delete("http://localhost:8080/users")
    yield


def test_kafka_user(browser: Browser, clear_database) -> None:
    page = browser.new_page(viewport=None, no_viewport=True)
    page.goto("http://localhost:5173/")

    expect(page.get_by_role("heading", name="No users found")).to_be_visible()

    requests.post(
        "http://localhost:8081/users",
        json={"name": "Vemund Santi", "email": "vemund@santi.no"},
    )

    page.reload()

    expect(
        page.locator("div")
        .filter(has_text=re.compile(r"^VSVemund Santivemund@santi\.no"))
        .first
    ).to_have_count(1)
