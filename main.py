import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import requests
from urllib.parse import urljoin
import time

load_dotenv()
form_link = "https://forms.gle/LFEA5jtfmLJhybgd9"
rental_website ="https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Defined"
}
base_url = "https://www.zillow.com"


class Research:
    def __init__(self):
        self.response = requests.get(url=rental_website, headers=headers)
        self.rental_link = self.response.text
        self.soup = BeautifulSoup(self.rental_link, "html.parser")
        self.driver = webdriver.Chrome()
        self.address_list = []
        self.price_list = []
        self.links_list = []

    def find_details(self):
        addresses = self.soup.find_all("address")
        prices = self.soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr")
        links = self.soup.find_all("a", {'data-test': 'property-card-link'})
        self.address_list = [address.getText() for address in addresses]
        self.price_list = [price.getText().strip("+ 1 bd/mo") for price in prices]
        self.links_list = [urljoin(base_url, link["href"]) for link in links]

    def fill_form(self):
        for n in range(len(self.address_list)):
            self.driver.get(form_link)
            time.sleep(3)
            try:
                self.driver.find_element(By.XPATH, os.getenv("ADDRESS_XPATH")).send_keys(self.address_list[n])
                self.driver.find_element(By.XPATH, os.getenv("PRICES_XPATH")).send_keys(self.price_list[n])
                self.driver.find_element(By.XPATH, os.getenv("LINKS_XPATH")).send_keys(self.links_list[n])
                self.driver.find_element(By.XPATH, os.getenv("SUBMIT_XPATH")).click()
            except Exception:
                pass
            time.sleep(2)


start = Research()
start.find_details()
start.fill_form()