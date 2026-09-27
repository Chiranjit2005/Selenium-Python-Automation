# Selenium E-Commerce Automation Framework

## 📌 Project Overview

This project is an **E-Commerce Web Automation Testing Framework** developed using **Python, Selenium WebDriver, PyTest, Page Object Model (POM), and data-driven testing**.

The framework automates the major user workflows of an online shopping application, including:

* Launching the browser
* User login
* Product search
* Adding products to the shopping cart
* Updating product quantity
* Verifying cart details
* Handling alerts, popups, and modal windows
* Capturing screenshots
* Reading test data from Excel/JSON
* Generating an HTML execution report

The project follows the **Page Object Model (POM)** design pattern to make the automation framework modular, reusable, maintainable, and scalable.

---

## 🌐 Application Under Test

**TutorialsNinja OpenCart Demo**

Application URL:

https://tutorialsninja.com/demo/

---

## 🛠️ Technologies Used

| Technology         | Purpose                       |
| ------------------ | ----------------------------- |
| Python             | Programming language          |
| Selenium WebDriver | Browser automation            |
| PyTest             | Test execution and assertions |
| Page Object Model  | Framework architecture        |
| Excel / JSON       | Test data management          |
| HTML               | Execution report              |
| Git                | Version control               |
| GitHub             | Source code repository        |
| Chrome WebDriver   | Browser automation            |

---

## ✨ Key Features

### 1. Browser Automation

The framework launches the Chrome browser and navigates to the application.

### 2. Login Automation

The framework supports login using registered user credentials.

### 3. Product Search

The framework searches for products and verifies that search results are displayed.

Example:

```text
Search Product → iPhone
```

### 4. Add to Cart

The framework identifies the first search result and adds the product to the shopping cart.

### 5. Update Quantity

The framework navigates to the shopping cart and updates the quantity of the selected product.

### 6. Cart Verification

The framework verifies:

* Product name
* Quantity
* Unit price
* Total price

### 7. Popup and Alert Handling

The framework handles:

* JavaScript alerts
* Bootstrap modal windows
* Cookie banners
* Success notifications

### 8. Screenshot Capture

Screenshots are captured during important test steps and failure scenarios.

### 9. Data-Driven Testing

Test data can be maintained externally using:

* Excel
* JSON

This prevents test data from being hard-coded inside the test cases.

### 10. HTML Test Report

After execution, the framework generates an HTML report containing:

* Test case name
* Execution status
* Test message
* Screenshot information
* Overall execution summary

---

# 📁 Project Structure

```text
selenium_capstone_v2/
│
├── config/
│   └── config.py
│
├── data/
│   ├── test_data.xlsx
│   └── test_data.json
│
├── tests/
│   ├── __init__.py
│   │
│   ├── test_ecommerce.py
│   │
│   └── pages/
│       ├── __init__.py
│       ├── login_page.py
│       ├── search_page.py
│       └── cart_page.py
│
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py
│   ├── screenshot.py
│   ├── excel_reader.py
│   ├── json_reader.py
│   ├── popup_handler.py
│   └── report_generator.py
│
├── reports/
│   └── execution_report.html
│
├── screenshots/
│   ├── 01_launch_browser.png
│   ├── 02_login.png
│   ├── 03_search.png
│   ├── 04_add_to_cart.png
│   ├── 05_update_quantity.png
│   ├── 06_verify_cart.png
│   └── ...
│
├── requirements.txt
├── pytest.ini
├── README.md
└── .gitignore
```

---

# 🏗️ Framework Architecture

The framework follows the **Page Object Model (POM)** architecture.

```text
                    ┌─────────────────────┐
                    │   test_ecommerce.py │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌────────────┐
       │ Login Page │   │ Search Page│   │ Cart Page  │
       └────────────┘   └────────────┘   └────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   Selenium WebDriver│
                    └─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ TutorialsNinja Demo │
                    └─────────────────────┘
```

---

# 📄 Page Object Model

## LoginPage

Responsible for:

* Opening login page
* Entering email
* Entering password
* Clicking login
* Verifying successful login

Example:

```python
login_page.login(email, password)
```

---

## SearchPage

Responsible for:

* Entering search keywords
* Clicking search
* Getting search results
* Selecting the first product
* Adding product to cart
* Checking cart counter
* Checking success message

Example:

```python
search_page.search("iPhone")
search_page.click_add_to_cart_first_result()
```

---

## CartPage

Responsible for:

* Opening cart
* Finding cart rows
* Reading product information
* Updating quantity
* Reading price
* Reading total
* Verifying cart contents

Example:

```python
cart_page.go_to_cart()
cart_page.update_quantity(0, 2)
```

---

# 🧪 Test Cases

| Test Case | Description         | Expected Result                          |
| --------- | ------------------- | ---------------------------------------- |
| TC01      | Launch Browser      | Application opens successfully           |
| TC02      | Login               | User successfully logs in                |
| TC03      | Search Product      | Product search results are displayed     |
| TC04      | Add Product to Cart | Product is added successfully            |
| TC05      | Update Quantity     | Product quantity is updated              |
| TC06      | Verify Cart Details | Product, quantity and price are verified |
| TC07      | Capture Screenshot  | Screenshot is generated                  |
| TC08      | Handle Popup/Alert  | Popup/alert is handled successfully      |

---

# 🔄 Test Execution Flow

```text
Start
  │
  ▼
Launch Browser
  │
  ▼
Open TutorialsNinja
  │
  ▼
Login
  │
  ▼
Search Product
  │
  ▼
Add Product to Cart
  │
  ▼
Open Cart
  │
  ▼
Update Quantity
  │
  ▼
Verify Cart Details
  │
  ▼
Handle Popup / Alert
  │
  ▼
Capture Screenshots
  │
  ▼
Generate HTML Report
  │
  ▼
End
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate into the project:

```bash
cd selenium_capstone_v2
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example dependencies:

```text
selenium
pytest
openpyxl
```

---

# 🔧 Configuration

Configuration values are maintained separately in:

```text
config/config.py
```

Example:

```python
BASE_URL = "https://tutorialsninja.com/demo/"

VALID_EMAIL = "your_registered_email"
VALID_PASSWORD = "your_password"

EXPLICIT_WAIT = 10
```

### Security Recommendation

Do not commit real passwords or API keys to GitHub.

Instead, use environment variables:

```python
import os

VALID_EMAIL = os.getenv("TEST_EMAIL")
VALID_PASSWORD = os.getenv("TEST_PASSWORD")
```

---

# ▶️ Running the Tests

## Run the complete test suite

```bash
pytest
```

---

## Run with verbose output

```bash
pytest -v
```

---

## Run a specific test file

```bash
pytest tests/test_ecommerce.py -v
```

---

## Run a specific test

Example:

```bash
pytest tests/test_ecommerce.py::TestECommerce::test_step3_search -v
```

---

# 📊 Test Reports

After execution, the framework generates an HTML report.

Example:

```text
reports/execution_report.html
```

The report contains:

```text
Total Tests
Passed
Failed
Skipped
Pass Percentage
Test Step
Status
Execution Message
Screenshot
```

Open the report in a browser to view the execution results.

---

# 📸 Screenshots

Screenshots are captured during important execution steps.

Example:

```text
screenshots/
│
├── 01_launch_browser.png
├── 02_login.png
├── 03_search.png
├── 04_add_to_cart.png
├── 05_update_quantity.png
├── 06_verify_cart.png
└── 08_popup_handling.png
```

Screenshots are particularly useful for debugging failed test cases.

---

# 📑 Data-Driven Testing

The framework supports external test data.

## Excel

Test data can be maintained in:

```text
data/test_data.xlsx
```

Example:

| Test Case | Product | Quantity |
| --------- | ------- | -------: |
| TC03      | iPhone  |        2 |

The framework reads the data using an Excel reader utility.

---

## JSON

Test data can also be maintained in:

```text
data/test_data.json
```

Example:

```json
{
    "product": "iPhone",
    "quantity": 2
}
```

---

# 🚨 Popup and Alert Handling

The project contains a dedicated popup handler:

```text
utils/popup_handler.py
```

It provides functionality for:

### JavaScript Alert

```python
handle_alert(driver)
```

### Cookie Banner

```python
dismiss_cookie_banner(driver)
```

### Bootstrap Modal

```python
close_modal(driver)
```

The modal handling is intentionally restricted to visible modal containers so that success alerts are not accidentally closed before they are verified.

---

# ⏱️ Explicit Waits

The framework uses Selenium explicit waits instead of relying heavily on `time.sleep()`.

Example:

```python
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(locator)
)
```

This improves test stability when elements load asynchronously.

---

# 🛡️ Exception Handling

The framework handles common Selenium exceptions such as:

```text
TimeoutException
NoSuchElementException
ElementClickInterceptedException
StaleElementReferenceException
UnexpectedAlertPresentException
```

When a test fails:

1. The error is logged.
2. A screenshot is captured.
3. The failure is reported.
4. The exception is raised so PyTest correctly marks the test as failed.

---

# 🔍 Robust Locator Strategy

The framework uses multiple locator strategies where necessary.

Examples:

```python
By.ID
By.NAME
By.XPATH
By.CSS_SELECTOR
```

For example, the cart rows use:

```python
//input[contains(@name,'quantity')]/ancestor::tr
```

with a fallback locator:

```python
//table//tbody/tr[.//input[contains(@name,'quantity')]]
```

This makes the framework more resilient to minor UI changes.

---

# 🧩 Utilities

## `driver_factory.py`

Responsible for creating and configuring the Selenium WebDriver.

---

## `screenshot.py`

Responsible for capturing screenshots during test execution.

---

## `excel_reader.py`

Reads test data from Excel files.

---

## `json_reader.py`

Reads test data from JSON files.

---

## `popup_handler.py`

Handles alerts, cookie banners, and modal dialogs.

---

## `report_generator.py`

Generates the final HTML execution report.

---

# 🧪 PyTest Fixtures

The framework uses PyTest fixtures for common setup and teardown activities.

Example:

```python
@pytest.fixture
def driver():
    driver = create_driver()
    yield driver
    driver.quit()
```

This ensures that the browser is properly closed after execution.

---

# 📌 Important Validation

The framework does not blindly continue after an Add-to-Cart failure.

Before updating the cart quantity, it verifies that:

```text
Product was added
        ↓
Cart contains product
        ↓
Cart row exists
        ↓
Quantity field exists
        ↓
Quantity is updated
```

This prevents errors such as:

```text
IndexError: No cart row at index 0
```

and produces a meaningful test failure instead.

---

# 🐞 Troubleshooting

## Browser does not start

Check:

```bash
python --version
pip show selenium
```

Make sure Selenium is installed correctly.

---

## Login fails

Verify:

* Registered email
* Registered password
* Application availability
* Login page locators
* Whether the demo site's user database has been reset

Do not automatically mark a genuine login failure as `SKIP`.

---

## Product is not added

Check:

* Search result exists
* Add-to-Cart button locator
* Success alert
* Cart counter

---

## Cart row not found

Check whether the product was actually added.

The framework checks:

```text
Cart rows
     ↓
Fallback cart rows
     ↓
Diagnostic message
```

---

## Quantity update fails

Check:

* Cart contains at least one product
* Quantity input exists
* Update button exists
* Page has finished loading

---

# 🔐 Security

Never commit credentials to GitHub.

Do not store:

```text
Passwords
API keys
Access tokens
Private credentials
```

inside:

```text
config.py
test_data.json
test_data.xlsx
```

For a public repository, use environment variables.

Add sensitive files to `.gitignore`:

```gitignore
.env
*.secret
credentials.json
```

---

# 📝 Example `.gitignore`

```gitignore
# Virtual environment
venv/
.venv/

# Python cache
__pycache__/
*.pyc

# PyTest
.pytest_cache/

# IDE
.vscode/
.idea/

# Environment variables
.env

# Generated reports
reports/*.html

# Screenshots
screenshots/*.png

# Sensitive test data
credentials.json
```

---

# 📈 Future Enhancements

The framework can be extended with:

* Cross-browser testing
* Firefox and Edge support
* Headless execution
* Selenium Grid
* Parallel execution
* Allure reporting
* CI/CD integration
* Jenkins integration
* GitHub Actions
* Logging framework
* Environment-specific configuration
* More comprehensive data-driven testing
* API automation
* Database validation

---

# 🎯 Learning Outcomes

This project demonstrates practical knowledge of:

* Selenium WebDriver
* Python automation
* PyTest
* Page Object Model
* XPath
* CSS selectors
* Explicit waits
* Exception handling
* Alert handling
* Popup handling
* Data-driven testing
* Screenshot automation
* HTML reporting
* Test framework design
* Git and GitHub

---

# 👨‍💻 Author

**Chiranjit Mandal**

B.Tech – Computer Science & Engineering

Institute of Engineering and Management, Kolkata

---

# 📜 License

This project is intended for educational, testing, and demonstration purposes.

---

## ⭐ Project Summary

This Selenium automation framework demonstrates an end-to-end E-Commerce testing workflow:

```text
Login
  ↓
Search Product
  ↓
Add to Cart
  ↓
Update Quantity
  ↓
Verify Cart
  ↓
Handle Popups
  ↓
Capture Screenshots
  ↓
Generate Report
```

The framework is designed using **Page Object Model + PyTest + Selenium WebDriver + Data-Driven Testing**, providing a structured foundation for scalable web automation testing.