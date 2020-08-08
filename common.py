import os
import csv
import json
import random
import string
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def create_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920,1080")
    user_agent = ''.join(string.ascii_lowercase[random.randint(i, 25)] for i in range(10))
    chrome_options.add_argument("user-agent={}".format(user_agent))
    return webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)


def get_beautiful_soup(driver, url):
    driver.get(url)
    return BeautifulSoup(driver.page_source, 'html.parser')


def create_folders(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        return list(csv.reader(csvfile))


def write_csv(file_path, content):
    create_folders(file_path)
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(content)


def write_csv_with_headers(file_path, content, headers):
    create_folders(file_path)
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(content)


def read_json(file_path):
    with open(file_path) as jsonfile:
        return json.load(jsonfile)


def write_json(file_path, content):
    create_folders(file_path)
    with open(file_path, 'w') as jsonfile:
        json.dump(content, jsonfile, indent=4, sort_keys=True)
