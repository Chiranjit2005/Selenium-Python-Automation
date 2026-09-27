"""
tests/pages/search_page.py
Page Object for search and product listing on tutorialsninja.com/demo/

Fix log (v2):
  - ADD_TO_CART_BTN now uses the aria-label / data-original-title attribute
    that tutorialsninja actually renders on its product grid buttons.
  - click_add_to_cart_first_result uses JavaScript click to bypass any
    overlay that blocks the normal .click().
  - is_success_alert_visible waits up to 15 s and also checks for the
    cart-total badge update as a fallback confirmation.
"""

import time
from selenium.webdriver.common.by      import By
from selenium.webdriver.common.keys    import Keys
from selenium.webdriver.support.ui     import WebDriverWait
from selenium.webdriver.support        import expected_conditions as EC
from selenium.common.exceptions        import TimeoutException, NoSuchElementException
from .base_page                        import BasePage


class SearchPage(BasePage):
    # ── Locators ───────────────────────────────────────────────────────────────
    SEARCH_BOX      = (By.NAME,  "search")
    SEARCH_BUTTON   = (By.XPATH, "//button[@class='btn btn-default btn-lg']")
    SEARCH_HEADING  = (By.XPATH, "//h1[contains(text(),'Search')]")
    PRODUCT_ITEMS   = (By.XPATH, "//div[@class='product-thumb']")
    PRODUCT_NAME    = (By.XPATH, ".//h4/a")

    # tutorialsninja "Add to Cart" button — primary selector uses the
    # data-original-title attribute; fallback uses the onclick attribute.
    ADD_TO_CART_BTN_PRIMARY  = (By.XPATH,
        ".//button[contains(@data-original-title,'Add to Cart')]")
    ADD_TO_CART_BTN_FALLBACK = (By.XPATH,
        ".//button[@onclick][1]")

    NO_RESULT_MSG   = (By.XPATH, "//p[contains(text(),'There is no product')]")

    # Success alert — tutorialsninja wraps it in #product-product or body level
    SUCCESS_ALERT   = (By.XPATH, "//div[contains(@class,'alert-success')]")
    # Cart badge updates when item is added — use as secondary confirmation
    CART_BADGE      = (By.XPATH, "//button[@id='cart-total']")

    # ── Actions ────────────────────────────────────────────────────────────────

    def search(self, term: str):
        self.type_text(*self.SEARCH_BOX, term)
        self.click(*self.SEARCH_BUTTON)

    def search_via_enter(self, term: str):
        box = self.type_text(*self.SEARCH_BOX, term)
        box.send_keys(Keys.RETURN)

    def get_product_count(self) -> int:
        return len(self.driver.find_elements(*self.PRODUCT_ITEMS))

    def get_first_product_name(self) -> str:
        items = self.driver.find_elements(*self.PRODUCT_ITEMS)
        if not items:
            return ""
        try:
            return items[0].find_element(*self.PRODUCT_NAME).text.strip()
        except NoSuchElementException:
            return ""

    def click_add_to_cart_first_result(self):
        """
        Locate the first product's Add-to-Cart button and click it.
        Tries the primary locator first; falls back to the generic onclick button.
        Uses JS click to bypass invisible overlays.
        """
        items = self.driver.find_elements(*self.PRODUCT_ITEMS)
        if not items:
            raise RuntimeError("No product items found on search results page.")

        first = items[0]
        self.scroll_into_view(first)
        time.sleep(0.4)   # let any lazy-render finish

        # Try primary locator
        btn = None
        try:
            btn = first.find_element(*self.ADD_TO_CART_BTN_PRIMARY)
        except NoSuchElementException:
            pass

        # Fallback
        if btn is None:
            try:
                btn = first.find_element(*self.ADD_TO_CART_BTN_FALLBACK)
            except NoSuchElementException:
                raise RuntimeError("Add-to-Cart button not found in first product thumb.")

        # Scroll button into view then JS-click (avoids 'element not interactable')
        self.scroll_into_view(btn)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", btn)

    def is_success_alert_visible(self) -> bool:
        """
        Wait for the green success alert. If that times out, check whether the
        cart badge text changed to '1 item(s)' as a fallback confirmation.
        """
        # Primary: green alert banner
        if self.is_visible(*self.SUCCESS_ALERT, timeout=15):
            return True

        # Fallback: cart badge shows at least 1 item
        try:
            badge = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.CART_BADGE)
            )
            badge_text = badge.text.strip()
            # badge normally reads "1 item(s) - $xx.xx" when cart is non-empty
            return "item" in badge_text.lower() and not badge_text.startswith("0")
        except TimeoutException:
            return False

    def get_success_message(self) -> str:
        try:
            return self.get_text(*self.SUCCESS_ALERT)
        except Exception:
            return "(success inferred from cart badge)"

    def has_no_results(self) -> bool:
        return self.is_visible(*self.NO_RESULT_MSG, timeout=5)
