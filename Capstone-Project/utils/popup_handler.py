"""
utils/popup_handler.py
Utilities for handling browser alerts, confirms, prompts,
and common overlay modals.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui        import WebDriverWait
from selenium.webdriver.support           import expected_conditions as EC
from selenium.common.exceptions           import (
    NoAlertPresentException, TimeoutException, NoSuchElementException
)
from selenium.webdriver.common.by         import By

from config.config import EXPLICIT_WAIT


def handle_alert(driver: WebDriver, action: str = "accept",
                 timeout: int = 5) -> str | None:
    """
    Wait for a JS alert / confirm / prompt and accept or dismiss it.
    Returns the alert text, or None if no alert appeared.
    """
    try:
        alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
        text  = alert.text
        print(f"  🔔  Alert detected: '{text}'")
        if action == "accept":
            alert.accept()
            print("  ✅  Alert accepted.")
        else:
            alert.dismiss()
            print("  ❌  Alert dismissed.")
        return text
    except TimeoutException:
        return None   # no alert — fine


def dismiss_cookie_banner(driver: WebDriver) -> None:
    """
    Click common 'Accept Cookies' buttons if present.
    Silently does nothing if no banner found.
    """
    selectors = [
        "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'accept')]",
        "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'agree')]",
        "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'got it')]",
        "//*[@id='cookieConsent']//button",
    ]
    for xpath in selectors:
        try:
            btn = driver.find_element(By.XPATH, xpath)
            btn.click()
            print("  🍪  Cookie banner dismissed.")
            return
        except NoSuchElementException:
            pass


def close_modal(driver: WebDriver, timeout: int = 5) -> bool:
    """
    Try to close a Bootstrap-style modal by clicking its × button.
    Returns True if a modal was closed.
    """
    close_xpaths = [
        "//button[contains(@class,'close')]",
        "//button[@data-dismiss='modal']",
        "//div[contains(@class,'modal')]//button[contains(@class,'close')]",
    ]
    for xpath in close_xpaths:
        try:
            btn = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            btn.click()
            print("  🪟  Modal closed.")
            return True
        except (TimeoutException, NoSuchElementException):
            pass
    return False
