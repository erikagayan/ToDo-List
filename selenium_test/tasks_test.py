from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()

url = "http://localhost:8000/"


def create_task(content, date_time, done=False):
    driver.get("http://localhost:8000/create/")

    content_input = driver.find_element(By.NAME, "content")
    content_input.send_keys(content)

    date_input = driver.find_element(By.NAME, "date_of_creation")
    date_input.send_keys(date_time)

    if done:
        done_checkbox = driver.find_element(By.NAME, "done")
        done_checkbox.click()

    tags_select = driver.find_element(By.ID, "id_tags")
    tags_options = tags_select.find_elements(By.TAG_NAME, "option")
    if tags_options:
        tags_options[0].click()

    submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    submit_button.click()
    time.sleep(3)


def update_task(task_id, new_content, new_date_time, done=False):
    driver.get(f"http://localhost:8000/{task_id}/update/")

    content_input = driver.find_element(By.NAME, "content")
    content_input.clear()
    content_input.send_keys(new_content)

    date_input = driver.find_element(By.NAME, "date_of_creation")
    date_input.clear()
    date_input.send_keys(new_date_time)

    done_checkbox = driver.find_element(By.NAME, "done")
    if done_checkbox.is_selected() != done:
        done_checkbox.click()

    submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    submit_button.click()
    time.sleep(3)


create_task("Test Task", "30102024" + Keys.TAB + "1400", done=True)
update_task(1, "Updated Task", "30102024" + Keys.TAB + "1530", done=True)

driver.quit()
