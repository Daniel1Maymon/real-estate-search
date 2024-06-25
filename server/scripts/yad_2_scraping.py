from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, random, re, json, os
from datetime import datetime

file_path = 'scrapet_data.json'
data_path = f'/home/daniel/projects/{file_path}'
data_from_file = []
item_ids = []

# Function to check if CAPTCHA is present
def is_captcha_present(browser):
    try:
        # Add the specific CAPTCHA identifier here (e.g., an image or a specific element related to CAPTCHA)
        captcha_element = browser.find_element(By.CSS_SELECTOR, 'div.captcha-wrapper')
        return True
    except NoSuchElementException:
        return False

# Function to create a randomized user agent
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Function to set up the Selenium WebDriver with options
def setup_browser():
    options = webdriver.FirefoxOptions()
    # options = webdriver.ChromeOptions()
    # Uncomment the next line to run in headless mode
    # options.add_argument("--headless")
    
    user_agent = get_random_user_agent()
    # print(f"ua = {user_agent}")
    
    options.set_preference("general.useragent.override", user_agent)
    
    # Optional: Add other preferences to make the browser appear more human
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)
    options.set_preference("general.platform.override", "")
    
    # Set up proxy if you have one
    # proxy = "your_proxy_address:port"
    # options.add_argument(f'--proxy-server={proxy}')
    
    # Create the browser instance
    browser = webdriver.Firefox(options=options)
    # browser = webdriver.Chrome(options=options)
    
    return browser

def add_timestamp(data):
    for item in data:
        if 'timestamp' not in item:
            item['timestamp'] = datetime.now().isoformat()
    return data

def write_data_to_file(data, filename=file_path):
    try:
        # Check if file exists
        file_exists = os.path.isfile(file_path)
        
        if file_exists:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
    
    except Exception as e:
        print(f"Error handling JSON file {file_path}: {e}")

def write_item_to_file(data, filename=file_path):
    try:
        # Check if file exists
        file_exists = os.path.isfile(file_path)
        
        existing_data = []
        if file_exists:
            with open(file_path, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
                item_ids = [item['item_id'] for item in data_from_file]
                print(f"item_ids = {item_ids}")
            
        # Append new data to existing data
        print(f"Checking if {data['item_id']} exists in the json file")
        if data['item_id'] not in item_ids:
            print(f"Adding item with {data['item_id']} to json file")
            existing_data.append(data)
            
            # Write JSON file
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(existing_data, file, ensure_ascii=False, indent=4)
        
        print(f"Data appended successfully to {file_path}")
                    
    except Exception as e:
        print(f"Error handling JSON file {file_path}: {e}")
    
def read_data_from_json(filepath):
    # global data_from_file  # Declare that we are using the global variable
    
    # if file exists, read from it:
    try: 
        # Check if file exists
        file_exists = os.path.isfile(file_path)
        
        if file_exists:
            with open(filepath, 'r', encoding='utf-8') as f:
                json_data = json.load(f)     
        
        number_of_data_items = len(json_data)   
        print(f"number_of_data_items = {number_of_data_items}")
    except Exception as e:
        print(f"Error handling JSON file {file_path}: {e}")
        
    return json_data if file_exists else []
    

def process_page(browser):
    try:
        data = {}
        
        # Open the target URL
        browser.get('https://www.yad2.co.il/realestate/forsale?topArea=2&area=11&city=6200&propertyGroup=apartments&price=1500000-1700000&Order=1') 

        # print(":: Searching the element <data-testid=feed-list>")

        # Wait for the specific <ul> element to be present
        element_list = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, '//ul[@data-testid="feed-list"]'))
        )
    
        # print(":: element_list FOUND (ul.feed-list_feed)")

        # Now, find all <li> elements with the data-testid="item-basic" attribute within the <ul>
        items = element_list.find_elements(By.XPATH, './/li[@data-testid="item-basic" or @data-testid="platinum-item"]')
        
        # print(':: items FOUND (.//li[@data-testid="item-basic"])')

        # Limit to the first five elements
        items = items[:5]
        # print("First 5 items =")
        for item in items:
            try:
                # print(item.get_attribute('outerHTML'))
                # Find the <span> element with the class "item-data-content_heading__tphH4" within each item
                item_address = item.find_element(By.CSS_SELECTOR, 'span.item-data-content_heading__tphH4')
                
                # Find the <span> element with the class "price_price__xQt90" within each item
                item_price = item.find_element(By.CSS_SELECTOR, 'span.price_price__xQt90')
                
                item_rooms_floor_size = item.find_elements(By.CSS_SELECTOR, 'span.item-data-content_itemInfoLine__AeoPP')[1]
                
                # a relative XPath that starts with a dot (.) indicates that the search should be relative to the current context (i.e., the item element).
                item_url = item.find_element(By.XPATH, './/a[@data-nagish="feed-item-layout-link"]').get_attribute('href')
                
                # Use a regular expression to extract the id from the url
                match = re.search(r'/item/([^?]+)\?', item_url)
                item_id = ""
                if match:
                    item_id = match.group(1) 
                
                print(f"\n{item_address.text[::-1]} | {item_rooms_floor_size.text[::-1]} | {item_id} | {item_price.text} | {item_url}\n")
                                
                data = {
                'item_id': item_id,
                'address': item_address.text,
                'price': item_price.text,
                'rooms_floor_size': item_rooms_floor_size.text,
                'url': item_url
                }
                
                write_item_to_file(data)
                
            except NoSuchElementException:
                print("One or more elements not found in item")

    except TimeoutException:
        print("Timeout occurred while waiting for the element.")
    except NoSuchElementException:
        print("The element was not found in the DOM.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_duplicate_from_file(filename=file_path):
    # 1. Read data from the file
    data = read_data_from_json(file_path)
    
    # 2.Delete duplicated item by id
    # For eac item, check if its id exist in ids
    ids = set()
    
    for item in data:
        if item['item_id'] not in ids:
            ids.add(item['item_id'])
            
        else:
            data.remove(item)
            

    # 3. Write updated data to the file
    write_data_to_file(data, filename=file_path)
    print()
    
# Function to perform the scraping
def scrape_yad2(attempts=5):
    
    if attempts == 0:
        print("Max attempts reached. CAPTCHA could not be bypassed.")
        return

    browser = setup_browser()
    
    try:
        process_page(browser)

        # Check if CAPTCHA is present, if so change the 'UserAgent'
        if is_captcha_present(browser):
            print("CAPTCHA detected, reloading page...")
            time.sleep(random.uniform(1, 5))
            browser.quit()
            scrape_yad2(attempts - 1)  # Decrement the attempts
        else:
            print("Processing complete, no CAPTCHA detected.")
            
    finally:
        browser.quit()
        # Add a delay before the next request
        # time.sleep(random.uniform(5, 10))

# Run the scraper

def main():
    data_from_file = read_data_from_json(data_path)
    
    # Add timestamp to each item
    updated_data = add_timestamp(data_from_file)
    
    # Write updated data back to JSON file
    write_data_to_file(updated_data, filename=file_path)
    delete_duplicate_from_file(filename=file_path)
    
    scrape_yad2()
    
if __name__ == "__main__":
    main()

    