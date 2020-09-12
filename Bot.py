from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class InstagramBot:
    def __init__(self, username, password):
        # Setup
        self.username = username
        self.password = password
        self.PATH = "C:\Program Files (x86)\chromedriver.exe"

        # launch Instagram
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get("https://instagram.com")
        time.sleep(2)

        # Login
        try:
            login_username = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            login_username.send_keys(username)
            time.sleep(2)

            login_password = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            login_password.send_keys(password)
            time.sleep(2)

            login_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button'))
            )
            login_button.click()
            time.sleep(2)

            not_now_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button'))
            )
            not_now_button.click()
            time.sleep(3)

            not_now_button_2 = WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[2]'))
            )
            not_now_button_2.click()
            time.sleep(2)
        except:
            print("Error When Trying To Login")

    def get_follow_count(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a') \
            .click()

        time.sleep(5)

        try:
            values = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, 'g47SY'))
            )

            print(f'You have  followers {values[1].text} \nYou are following {values[2].text} people')
        except:
            print('Error When Getting Follow Count')

    def get_not_follow_back(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a')\
            .click()

        try:
            following = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a'))
            )
            following.click()
        except:
            print("Error opening following")

        following = self._get_names()

        time.sleep(10)

        try:
            followers = WebDriverWait(self.driver, 1000).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a'))
            )
            followers.click()
        except:
            print("Error opening followers")

        followers = self._get_names()

        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)

    def _get_names(self):
        time.sleep(2)
        suggestions = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        self.driver.execute_script('arguments[0].scrollIntoView()', suggestions)
        time.sleep(4)
        try:
            scroll_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]'))
            )
            last_height, height = 0, 1
            while last_height != height:
                last_height = height
                time.sleep(1)
                height = self.driver.execute_script("""
                                         arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                                         return arguments[0].scrollHeight;
                                         """, scroll_box)
                links = scroll_box.find_elements_by_tag_name('a')
                names = [name.text for name in links if name.text != '']
            # close button
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button") \
                .click()
            return names
        except:
            print("Get names error")

