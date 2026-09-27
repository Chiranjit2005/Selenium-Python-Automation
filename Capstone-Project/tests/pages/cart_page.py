"""
tests/pages/cart_page.py
Page Object for the Shopping Cart on tutorialsninja.com/demo/

Fix log (v2):
  - go_to_cart: navigate directly via URL as primary path; dropdown as fallback.
    This avoids the TimeoutException on #cart-total when the badge hasn't
    re-rendered after a fresh add-to-cart.
  - CART_ROWS: now targets the product rows specifically (excludes summary rows).
  - QTY_INPUT: tutorialsninja cart uses <input name="quantity"> inside a <td>
    that has no unique class. Added multiple fallback selectors.
  - UPDATE_BTN / column indices updated to match tutorialsninja's real DOM.
"""

import time
from selenium.webdriver.common.by      import By
from selenium.webdriver.support.ui     import WebDriverWait
from selenium.webdriver.support        import expected_conditions as EC
from selenium.common.exceptions        import TimeoutException, NoSuchElementException
from .base_page                        import BasePage
from config.config                     import EXPLICIT_WAIT, BASE_URL


CART_URL = BASE_URL.rstrip("/") + "/index.php?route=checkout/cart"


class CartPage(BasePage):
    # ── Locators ───────────────────────────────────────────────────────────────
    # Navigation
    CART_BUTTON    = (By.ID,    "cart-total")          # <button id="cart-total">
    VIEW_CART_LINK = (By.XPATH, "//a[contains(@href,'checkout/cart')]")

    # Cart table — tutorialsninja's cart table has id="checkout-cart"
    # Product rows are <tr> elements that contain an input[name='quantity']
    # (summary/total rows do NOT have quantity inputs — this filter is key)
    CART_ROWS = (By.XPATH,
        "//form[@id='form-cart']//tbody/tr[.//input[@name='quantity']]")

    # Fallback if the form id isn't present
    CART_ROWS_FALLBACK = (By.XPATH,
        "//div[@id='checkout-cart']//tbody/tr[.//input[@name='quantity']]")

    # Within each row (relative XPaths)
    PRODUCT_NAME_CELL = (By.XPATH, ".//td[2]//a")
    # qty input — tutorialsninja renders it as:
    #   <input type="text" name="quantity" value="1" size="3" ...>
    QTY_INPUT         = (By.XPATH, ".//input[@name='quantity']")
    # Update button: rendered as <button type="submit" data-original-title="Update">
    UPDATE_BTN_PRIMARY  = (By.XPATH, ".//button[@data-original-title='Update']")
    UPDATE_BTN_FALLBACK = (By.XPATH, ".//button[contains(@onclick,'cart.update')]")
    # Column positions (1-based) in the product row: name=2, model=3, qty=4, price=5, total=6
    UNIT_PRICE_CELL   = (By.XPATH, ".//td[5]")
    TOTAL_CELL        = (By.XPATH, ".//td[6]")

    # Page-level
    EMPTY_CART_MSG = (By.XPATH, "//p[contains(text(),'Your shopping cart is empty')]")
    SUCCESS_ALERT  = (By.XPATH, "//div[contains(@class,'alert-success')]")

    # ── Actions ────────────────────────────────────────────────────────────────

    def go_to_cart(self):
        """
        Navigate to the cart page. Tries the direct URL first (most reliable),
        then falls back to the cart dropdown button.
        """
        try:
            self.driver.get(CART_URL)
            # Wait until at least the checkout-cart div is present
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.ID, "checkout-cart"))
            )
        except TimeoutException:
            # Fallback: click the cart button in the navbar
            self._go_via_button()

    def _go_via_button(self):
        try:
            btn = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.element_to_be_clickable(self.CART_BUTTON)
            )
            btn.click()
            time.sleep(0.8)
            view_link = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.element_to_be_clickable(self.VIEW_CART_LINK)
            )
            view_link.click()
        except TimeoutException:
            # Last resort: hard navigate
            self.driver.get(CART_URL)

    def get_cart_rows(self):
        """Return all product rows (rows that have a quantity input)."""
        rows = self.driver.find_elements(*self.CART_ROWS)
        if not rows:
            rows = self.driver.find_elements(*self.CART_ROWS_FALLBACK)
        return rows

    def get_cart_item_count(self) -> int:
        return len(self.get_cart_rows())

    def get_first_product_name(self) -> str:
        rows = self.get_cart_rows()
        if not rows:
            return ""
        try:
            return rows[0].find_element(*self.PRODUCT_NAME_CELL).text.strip()
        except NoSuchElementException:
            # Generic fallback: second cell text
            try:
                return rows[0].find_elements(By.TAG_NAME, "td")[1].text.strip()
            except Exception:
                return ""

    def _find_qty_input(self, row):
        """Return the quantity input element within a row, with fallback."""
        try:
            return row.find_element(*self.QTY_INPUT)
        except NoSuchElementException:
            # Try any text/number input inside the row
            for inp in row.find_elements(By.TAG_NAME, "input"):
                t = inp.get_attribute("type") or ""
                if t in ("text", "number", ""):
                    return inp
            raise NoSuchElementException("Quantity input not found in row")

    def _find_update_btn(self, row):
        try:
            return row.find_element(*self.UPDATE_BTN_PRIMARY)
        except NoSuchElementException:
            try:
                return row.find_element(*self.UPDATE_BTN_FALLBACK)
            except NoSuchElementException:
                # Any submit button inside the row
                btns = row.find_elements(By.XPATH, ".//button[@type='submit']")
                if btns:
                    return btns[0]
                raise NoSuchElementException("Update button not found in row")

    def update_quantity(self, row_index: int = 0, quantity: int = 2):
        rows = self.get_cart_rows()
        if row_index >= len(rows):
            raise IndexError(f"No cart row at index {row_index}")
        row       = rows[row_index]
        qty_input = self._find_qty_input(row)
        qty_input.clear()
        qty_input.send_keys(str(quantity))
        update_btn = self._find_update_btn(row)
        self.scroll_into_view(update_btn)
        self.driver.execute_script("arguments[0].click();", update_btn)
        time.sleep(2.0)   # wait for page refresh after update

    def get_quantity(self, row_index: int = 0) -> str:
        rows = self.get_cart_rows()
        if row_index >= len(rows):
            return "0"
        try:
            return self._find_qty_input(rows[row_index]).get_attribute("value") or "0"
        except Exception:
            return "0"

    def get_unit_price(self, row_index: int = 0) -> str:
        rows = self.get_cart_rows()
        if row_index >= len(rows):
            return "$0.00"
        try:
            return rows[row_index].find_element(*self.UNIT_PRICE_CELL).text.strip()
        except NoSuchElementException:
            cells = rows[row_index].find_elements(By.TAG_NAME, "td")
            return cells[4].text.strip() if len(cells) > 4 else "$0.00"

    def get_row_total(self, row_index: int = 0) -> str:
        rows = self.get_cart_rows()
        if row_index >= len(rows):
            return "$0.00"
        try:
            return rows[row_index].find_element(*self.TOTAL_CELL).text.strip()
        except NoSuchElementException:
            cells = rows[row_index].find_elements(By.TAG_NAME, "td")
            return cells[-1].text.strip() if cells else "$0.00"

    def is_cart_empty(self) -> bool:
        return self.is_visible(*self.EMPTY_CART_MSG, timeout=5)

    def is_update_success(self) -> bool:
        return self.is_visible(*self.SUCCESS_ALERT, timeout=10)
