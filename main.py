import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import filedialog


red_text = "\033[31mRed Text\033[0m"
green_text = "\033[32mGreen Text\033[0m"
yellow_text = "\033[33mYellow Text\033[0m"

def find_element(single_element,name):
    try:
        elements_name = single_element.find_all(class_=name)
        array = []
        for element_name in elements_name:
            temp = element_name.text
            array.append(temp)
        return array
    except Exception as e:
        print("An error occurred at finding element:", e)
        raise ValueError("couldn't find a element. Relaunch the exe")
        

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
        raise ValueError("couldn't find a element. Relaunch the exe")
def choose_save_location():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
        title="Save Screenshot As"
    )

    return file_path
def export_to_json(data, file_name):
    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data exported to '{file_name}' as JSON successfully.")
    except Exception as e:
        print("An error occurred while exporting:", e)

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

links=[]
games_name=[]
games_date=[]
images=[]
links=find_element_tag(single_element,'a','href')
full_links=['https://store.epicgames.com'+element for element in links]

games_name=find_element(single_element,'css-1h2ruwl')
games_date=find_element(single_element,'css-nf3v9d')
images=find_element_tag(single_element,'img','data-image')
print("info!!!")
print("**********************************")
print("**********************************")
print("{{Links}}",full_links)
print("{{Name}}",games_name)
print("{{Date}}",games_date)
print("{{Image Links}}",images)
print("**********************************")
print("**********************************")


driver.quit()

# Combine arrays into a dictionary
combined_data = {
    'games_name': games_name,
    'games_date': games_date,
    'image_urls': images
}

# Call the function to export the combined data as JSON
export_to_json(combined_data, '_export/output.json')

#at line 112 is not very effective to write like that but it works
#TODO Make a better way of writing line 112
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
<div class="container">
        <div class="logo">
            <img src="logo.png" alt="epic">
            <h2>Free Gaming</h2>
        </div>
    <div class="flex-container">
        <!-- Loop through the games data -->
        {"".join(f'''
        <div class="game-info">
            <div class="head"><p>{game_name}</p></div>
            
            <div class="images">
                <img src="{image_url}" alt="Game Image">
                {'<div class="alert_p"><p>Free Now</p></div>' if 'Free Now' in game_date else '<div class="alert_p coming_soon"><p>Coming Soon</p></div>'}
            </div>
            <p>{game_date.replace("Free ", 'Free At: ').replace("Free At: Now", '<span class="highlight">Free Now Until</span>')}</p>
        </div>
        ''' for game_name, game_date, image_url in zip(combined_data['games_name'], combined_data['games_date'], combined_data['image_urls']))}
    </div>
    </div>
</body>
</html>
"""

try:
    with open("_web/index.html", "w") as html_file:
        html_file.write(html_content)
    print("\nHTML file created successfully!")
except Exception as e:
    print("\nAn error occurred:", str(e))
    print("Failed to create HTML file.")

# Use Selenium to capture a screenshot of the rendered HTML content
driver = webdriver.Chrome(options=chrome_options)
driver.get('file://' + os.path.abspath("_web/index.html"))  # Load the local HTML file

total_height_script = "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
total_content_height = driver.execute_script(total_height_script)

total_width_script = "return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );"
total_content_width = driver.execute_script(total_width_script)

# Set the browser window size to the desired resolution (width x height)
desired_width = total_content_width-5
desired_height = total_content_height-5  # Add some buffer for potential scrollbars
driver.set_window_size(desired_width, desired_height)

screenshot = driver.get_screenshot_as_png()

driver.quit()

# Convert the screenshot to an Image object using Pillow
screenshot_image = Image.open(BytesIO(screenshot))

# Ask the user for the save location
file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        initialfile="freeEpicGames.png",  # Default name
        filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
        title="Save PNG As"
    )

if file_path:
    screenshot_image.save(file_path,dpi=(300, 300))
    print(f"Screenshot saved as {file_path}")
else:
    print("Screenshot not saved.")

# Display a prompt and wait for user input
input("Script finished. Press Enter to close...")
