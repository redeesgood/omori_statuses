from playwright.sync_api import Page, Locator

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        
        self.status_btn: Locator = page.locator("#check-status-btn")
        self.status_box: Locator  = page.locator("#character-status")
        
        self.upload_input: Locator  = page.locator("#mission-upload")
        self.upload_btn: Locator  = page.locator("#upload-btn")
        self.upload_message: Locator  = page.locator("#upload-message")
        self.download_link: Locator  = page.locator("#download-report")
        
    def request_agent_status(self):
        self.status_btn.click()
        
    def upload_document(self, file_path: str):
        self.upload_input.set_input_files(file_path)
        self.upload_btn.click()
        
        
        