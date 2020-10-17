import re
import urllib

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import warnings
from selenium.webdriver.support import expected_conditions as ec
from urllib.parse import urljoin, urlparse, parse_qs
from mobbin_crawler.mobbin_scrapy.models import MobbinImageModel
from email.message import Message


MOBBIN_DEFAULT_TIMEOUT = 15
MOBBIN_BASE_URL = "http://mobbin.design/"


def get_url_from_mail_to(mail_to_url):
    try:
        body = re.search(r'body=(.*?)&subject=', mail_to_url).group(1)
    except AttributeError:
        try:
            body = re.search(r'body=(.*?)&amp;subject=', mail_to_url).group(1)
        except AttributeError:
            body = re.search(r'body=(.*?)&', mail_to_url).group(1)
    url = urllib.parse.unquote(body)
    return str(url)


class MobbinHandle:
    def __init__(self, driver):
        self.driver = driver

    def manual_login(self):
        self.driver.get(MOBBIN_BASE_URL)
        input("press enter if login complete...")

    def auto_login(self):
        # LOAD CREDENTIALS
        from credentials.credentials_loader import load_google_credentials
        cred = load_google_credentials()

        # Save main window for handling pop up window
        main_window_handle = None
        while not main_window_handle:
            main_window_handle = self.driver.current_window_handle

        #  Load main page
        self.driver.get(MOBBIN_BASE_URL)

        # Click login button
        try:
            # Large screen login button
            login_button = self.driver.find_element_by_xpath(
                '//button[@class="sc-bFADNz ctxfBC sc-dnqmqq dKFGsJ"]')
            login_button.click()
        except:
            # Small button login button
            login_button = self.driver.find_element_by_xpath("//h3[@class='sc-iybRtq khIrQf']")
            login_button.click()

        # sc-iybRtq khIrQf
        # WebDriverWait(self.driver, 10).until(ec.invisibility_of_element_located(login_button))
        sleep(1)

        # After login options shows up, click google login
        google_login_button = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div/div[2]/button[1]')
        google_login_button.click()

        # POP up window for Google sign in will open
        # Get Pop up window
        signin_window_handle = None
        while not signin_window_handle:
            for handle in self.driver.window_handles:
                if handle != main_window_handle:
                    signin_window_handle = handle
                    break

        # Switch to popup window
        self.driver.switch_to.window(signin_window_handle)
        WebDriverWait(self.driver, MOBBIN_DEFAULT_TIMEOUT).until(ec.visibility_of_element_located((By.ID, "view_container")))

        #     ON Google Auth page
        emailElem = self.driver.find_element_by_id('identifierId')
        emailElem.send_keys(cred["ID"])
        nextButton = self.driver.find_element_by_id('identifierNext')
        nextButton.click()
        sleep(3)

        passwordElem = self.driver.find_element_by_xpath('//input[@type="password"]')
        passwordElem.send_keys(cred["PW"])
        signinButton = self.driver.find_element_by_id('passwordNext')
        signinButton.click()
        sleep(5)

        self.driver.switch_to.window(main_window_handle)  # or driver.switch_to_default_content()

    def scroll_to_bottom(self) -> bool:
        try:
            bottom_loading_indicator = self.driver.find_element_by_xpath(
                "//div[@class='sc-jKmXuR fiuBLV']")
            self.driver.execute_script("arguments[0].scrollIntoView();",
                                       bottom_loading_indicator)
            return True
        except NoSuchElementException as e:
            warnings.warn(e.msg)
            return False

    def get_all_screen_divs(self):
        """
        currently available in Patterns page
        :return:
        """
        # on Patterns page
        screens_divs = self.driver.find_element_by_xpath("//div[@class='sc-gNJABI dxMWgA']")
        return screens_divs

    def get_n_screen_div(self, n: int):
        result = {"success": False,
                  "value": None}
        try:

            xpath = "//div[@class='sc-gldTML iwZekx sc-drKuOJ fLePfb row']/div[{0}]".format(n+1)
            # WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))
            div = self.driver.find_element_by_xpath(xpath)
            print(div)
            # n + 1 :: xpath starts counting from 1
            result["success"] = True
            result["value"] = div
        except NoSuchElementException as e:
            result["success"] = False
            # warnings.warn(e.msg)
            print(e.msg)
        return result

    def go_pattern_detail(self):
        raise NotImplementedError

    def parse_detail(self) -> MobbinImageModel:
        # Crawl Data from detail view
        app_name_text = self.driver.find_element_by_xpath("//h1[@class='sc-keFjpB jMBnlD']").text
        app_desc_text = self.driver.find_element_by_xpath("//h1[@class='sc-jWojfa RtCwr']").text
        app_url_text = self.driver.find_element_by_xpath("//div[@class='sc-jkCMRl eyWWVY']/a").get_attribute("href")
        app_url_text = urljoin(MOBBIN_BASE_URL, app_url_text)

        email_to_url = self.driver.find_element_by_xpath("//a[@class='sc-dxgOiQ dtyrSn']").get_attribute("href")
        print(email_to_url)
        url = get_url_from_mail_to(email_to_url)


        screenshot_img = self.driver.find_element_by_xpath("//img[@class='sc-dznXNo cHYHvz']").get_attribute("src")
        meta_container = self.driver.find_element_by_xpath("//div[@class='sc-cpHetk irphtn']")
        meta_patterns = meta_container.find_elements_by_xpath("./div[1]//button")
        meta_patterns_texts = [meta_pattern.text for meta_pattern in meta_patterns]
        meta_elements = meta_container.find_elements_by_xpath("./div[2]//button")
        meta_elements_texts = [meta_element.text for meta_element in meta_elements]

        # Assign to model data
        mobbin_image_data = MobbinImageModel()
        mobbin_image_data.app = app_name_text
        mobbin_image_data.app_desc = app_desc_text
        mobbin_image_data.app_url = app_url_text
        mobbin_image_data.category = ""
        mobbin_image_data.file_url = screenshot_img
        mobbin_image_data.image_id = ""
        mobbin_image_data.mobbin_elements = meta_elements_texts
        mobbin_image_data.mobbin_patterns = meta_patterns_texts
        mobbin_image_data.url = url

        print(meta_elements_texts)
        print(meta_patterns_texts)

        return mobbin_image_data



