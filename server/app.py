# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as webdriver
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC

# browser = webdriver.Chrome()
# browser.get("https://www.yad2.co.il/realestate/forsale?topArea=2&area=11&city=6200&propertyGroup=apartments&price=1500000-1700000&Order=1")

import chromedriver_autoinstaller
from selenium import webdriver

# Install ChromeDriver if not already installed
chromedriver_autoinstaller.install()

# Now you can use ChromeDriver as usual
driver = webdriver.Chrome()

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Optional: Run in headless mode
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--disable-software-rasterizer")
# chrome_options.binary_location = '/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe'

# browser = webdriver.Chrome(options=chrome_options)

# browser.get("https://www.yad2.co.il/realestate/forsale?topArea=2&area=11&city=6200&propertyGroup=apartments&price=1500000-1700000&Order=1")
# browser.save_screenshot("screenshot.png")
    
# Using Selenium - a headless browser (CAPTCHA Solving Service)
# def execute_selenium():
#     # Initialize the WebDriver: 
#     # instance of ChromeOptions
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--use_subprocess")

#     # instance of Chrome
#     browser = webdriver.Chrome(options=chrome_options)

# Function to scrape data from Yad2
def scrape_yad2():
    
    # handling CAPTCHA
    # execute_selenium()
    
    url = 'https://www.yad2.co.il/realestate/forsale?topArea=2&area=11&city=6200&propertyGroup=apartments&price=1500000-1700000&Order=1'

    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        platinum_items = soup.find_all('li', {'data-testid': 'platinum-item', 'data-nagish': 'feed-item-list-box'})

# Function to scrape quotes
def scrape_quotes():
    # URL of the website to scrape
    url = 'http://quotes.toscrape.com/'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all quote containers
        quote_containers = soup.find_all('div', class_='quote')

    


        # Iterate over each quote container
        for quote in quote_containers:
            # Extract the text of the quote and the author
            quote_text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text

            # Extract the tags of the quote
            tags_element = quote.find('div', class_='tags').find_all('a', class_='tag')
            
            tags = [tag.text for tag in tags_element]

            # Print the quote and author
            print(f'Quote: {quote_text}')
            print(f'Author: {author}')
            print(f"tags: {tags}")
            print('---')
            
                

    else:
        print(f'Error fetching data. Status code: {response.status_code}')

# Run the function to scrape quotes
if __name__ == '__main__':
    # scrape_quotes()
    scrape_yad2()
