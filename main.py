from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def find_element(single_element,name):
    try:
        elements_name = single_element.find_all(class_=name)
        array = []
        for element_name in elements_name:
            temp = element_name.text
            array.append(temp)
        return array
    except Exception as e:
        print("couldn't find a element. returning empty array")
        print("An error occurred at finding element:", e)
        return []

def find_element_tag(single_element,name,tag):
    try:
        elements_tags = single_element.find_all(name)
        array = []
        for element_tag in elements_tags:
            element_src = element_tag.get(tag)
            array.append(element_src)
        return array
    except Exception as e:
        print("couldn't find a element with a tag. returning empty array")
        print("An error occurred at finding element with tags:", e)
        return []

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # This line enables headless mode
#My brother in christ i need to write this extra to make it so it will run in headless mode
chrome_options.add_argument("--disable-features=InterestCohort")
chrome_options.add_argument("--disable-features=PermissionsPolicy")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")


# Set up Selenium WebDriver (ChromeDriver)
driver = webdriver.Chrome(options=chrome_options)

url = 'https://store.epicgames.com/en-US/'
driver.get(url)

# Wait for the page to load completely
wait = WebDriverWait(driver, 30)  # Maximum wait time of 10 seconds
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'span')))

page_source = driver.page_source

# Parse with Beautiful Soup
soup = BeautifulSoup(page_source, "html.parser")

# # Find the first element with the specified class
single_element = soup.find(class_='css-1p2cbqg')

games_name=[]
games_date=[]
image=[]

games_name=find_element(single_element,'css-1h2ruwl')
games_date=find_element(single_element,'css-nf3v9d')
image=find_element_tag(single_element,'img','data-image')
print(games_name)
print(games_date)
print(image)


driver.quit()

