from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re


def terms(url):
    # create a new Chrome session
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(30)
    driver.get(url)

    if "Page not found" in driver.title:
        driver.quit()
        return False

    else:
        # find the gfycat link
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        all_terms = soup.find_all("div", {"class": "Pitchergif"})
        gif = [gif.replace('"', '') for gif in re.findall('ifr/(.*) scrolling', str(all_terms))]

        # find the pitch type
        pitch_count = 0
        pitches = []
        for pitch_tag in soup.find_all("h2", {"class": "ng-binding"}):
            pitches.append(pitch_tag.text)
            pitch_count += 1

        # find the pitch speed
        speeds = []
        count = 1
        for speed_tag in soup.find_all("b", {"class": "ng-binding"}):
            if count % 2 == 0:
                speeds.append(speed_tag.text)
                count += 1
            else:
                count += 1

        # find the pitcher's age
        age_tag = soup.find_all("h3", {"class": "ng-binding"})
        age = [str(re.findall('</b> (.*) \(', str(age_tag))[0])] * pitch_count


        driver.quit()

        return gif, pitches, speeds, age
