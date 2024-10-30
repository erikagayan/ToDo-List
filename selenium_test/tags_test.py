from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

url = "http://localhost:8000/"


def create_tag(tag_name):
    driver.get(url + "tags/create/")
    tag_input = driver.find_element(By.NAME, "name")
    tag_input.send_keys(tag_name)
    tag_input.send_keys(Keys.RETURN)
    time.sleep(5)
    assert tag_name in driver.page_source


def update_tag(old_name, new_name):
    driver.get(url + "tags/")
    update_button = driver.find_element(By.LINK_TEXT, "Update")
    update_button.click()
    tag_input = driver.find_element(By.NAME, "name")
    tag_input.clear()
    tag_input.send_keys(new_name)
    tag_input.send_keys(Keys.RETURN)
    time.sleep(5)
    assert new_name in driver.page_source and old_name not in driver.page_source


def delete_tag(tag_name):
    driver.get(url + "tags/")
    delete_button = driver.find_element(By.LINK_TEXT, "Delete")
    delete_button.click()

    confirm_button = driver.find_element(
        By.XPATH, "//input[@type='submit' and @value='Yes']"
    )
    confirm_button.click()

    time.sleep(5)
    assert tag_name not in driver.page_source


create_tag("TestTag")
update_tag("TestTag", "UpdatedTag")
delete_tag("UpdatedTag")

driver.quit()
