import json
import os
import pytest
import allure
from playwright.sync_api import Page, Route, expect

@pytest.mark.parametrize("state, heart_rate, css_class", [
    ("Спокоен", 75, "calm"),
    ("Тревога", 110, "stress"),
    ("ПАНИКА", 180, "panic")
])
def test_psycho_status(page: Page, dashboard_page, state, heart_rate, css_class):
    def mock_status(route: Route):
        fake_response = {
            "state": state,
            "heart_rate": heart_rate,
            "css_class": css_class
        }
        
        route.fulfill(
            status=200,
            content_type="application/json; charset=utf-8",
            body=json.dumps(fake_response)
        )
        
    page.route("**/status", mock_status)
    
    dashboard_page.request_agent_status()
    
    expected_text = f"Состояние: {state} | Пульс: {heart_rate}"
    
    expect(dashboard_page.status_box).to_have_text(expected_text)
    expect(dashboard_page.status_box).to_have_class(f"character-box {css_class}")
    
    allure.attach(
        page.screenshot(),
        name = f"Финальный результат_{state}",
        attachment_type=allure.attachment_type.PNG
    )
    
def test_documents_workflow(page: Page, dashboard_page):
    test_file = "secret_plan.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("План операции: проникнуть на базу")
        
    dashboard_page.upload_document(test_file)
    
    expect(dashboard_page.upload_message).to_have_text("Файл успешно загружен в базу!") 
    
    os.remove(test_file)
    
    with page.expect_download() as download_info:
        dashboard_page.download_link.click()
        
    download = download_info.value
    file_name = download.suggested_filename
    
    os.makedirs("downloads", exist_ok=True),
    save_path = f"downloads/{file_name}"
    download.save_as(save_path)
    
    assert os.path.exists(save_path) is True   