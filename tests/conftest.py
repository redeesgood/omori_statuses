import os
import pytest

from playwright.sync_api import Page
from pages.base_page import BasePage

@pytest.fixture
def dashboard_page(page: Page):
    # Фикстура открывает наш локальный index.html и возвращает 
    # готовый объект Page Object для тестов.
    
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_file_path = os.path.join(current_dir, "app", "index.html")
    
    file_url = f"file://{html_file_path}"
    
    page.goto(file_url)
    
    return BasePage(page)

