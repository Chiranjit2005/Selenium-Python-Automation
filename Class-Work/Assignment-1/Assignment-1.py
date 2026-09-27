            #1
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver=webdriver.Chrome()

driver.get("https://testautomationpractice.blogspot.com/")

driver.find_element(By.ID,"name").send_keys("Arka Pan")

driver.find_element(By.NAME,"input1").send_keys("very good")

time.sleep(2)
driver.find_element(By.TAG_NAME,"input").clear()
time.sleep(2)

driver.find_element(By.CLASS_NAME,"form-check-inline").click()
driver.find_element(By.LINK_TEXT,"Udemy Courses").click()


time.sleep(5)
driver.quit()

              #2
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
driver=webdriver.Chrome()

driver.get("https://testautomationpractice.blogspot.com/")

elements=driver.find_elements(By.TAG_NAME,"a")

for i in elements:
    print(i.text)

time.sleep(2)
driver.quit()

             #3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
driver=webdriver.Chrome()

driver.get("https://testautomationpractice.blogspot.com/")

elements=driver.find_elements(By.CSS_SELECTOR, "*[id^='a']")

for i in elements:
    print(i.text)


time.sleep(2)
driver.quit()

                 #4
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
driver=webdriver.Chrome()

driver.get("https://testautomationpractice.blogspot.com/")

driver.find_element(By.CSS_SELECTOR,"div.form-group > input.form-control").send_keys("Chiranjit")

driver.find_element(By.CSS_SELECTOR,"div.widget-content > ul > li > a[href*='udemy']").click()

time.sleep(2)
driver.quit()