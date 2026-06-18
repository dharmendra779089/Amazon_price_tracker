from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import time

# 1. Setup your URLs
# Configured for Amazon India (.in)
live_url = "https://www.amazon.in/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
formspree_url = "https://formspree.io/f/your_form_id_here" 

# 2. Configure Selenium WebDriver
chrome_options = Options()

# Spoof the User-Agent to look like a real browser. This is crucial for bypassing 
# initial Amazon anti-bot checks.
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

# Uncomment the line below if you want the browser to run invisibly in the background.
# Leaving it commented out is helpful for debugging so you can watch what the bot is doing.
# chrome_options.add_argument("--headless=new") 

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to the Amazon page. Selenium will naturally wait for the base page to load.
    driver.get(live_url)
    
    # Pause for 2 seconds to allow any dynamic JavaScript pricing scripts to finish executing
    time.sleep(2)
    
    # Target fallback hierarchy to find the price element across varying Amazon UI layouts
    price_selectors = [
        (By.CLASS_NAME, "a-price-whole"),
        (By.CLASS_NAME, "a-offscreen"),
        (By.ID, "priceblock_ourprice")
    ]
    
    raw_price = None
    
    # Iterate through our list of strategies to find the price
    for by, value in price_selectors:
        try:
            price_element = driver.find_element(by, value)
            
            # Note: Selenium's standard `.text` method sometimes returns an empty string 
            # if the element is visually hidden by CSS (like 'a-offscreen'). 
            # Using `.get_attribute("textContent")` forces it to read the raw HTML text.
            raw_price = price_element.get_attribute("textContent").strip()
            
            # If we successfully grabbed a string, break out of the search loop
            if raw_price:
                break
        except NoSuchElementException:
            # If the element isn't found, ignore the error and try the next selector in the list
            continue
            
    # Verify an element was matched before executing string manipulations
    if raw_price:
        
        # Comprehensive Sanitization: Strips currency characters (₹, $), commas, and whitespace
        clean_price_string = "".join(char for char in raw_price if char.isdigit() or char == '.')
        
        # Strip any trailing decimal marks often left behind by the 'a-price-whole' container
        if clean_price_string.endswith('.'):
            clean_price_string = clean_price_string[:-1]
            
        try:
            price_as_float = float(clean_price_string)
            print(f"Current price parsed successfully: ₹{price_as_float}")
            
            # 3. Evaluation Logic
            alert = False
            target_threshold = 10000.00  # Threshold cap set for Indian Rupees (INR)
            
            if price_as_float < target_threshold: 
                alert = True
                
            # 4. Outbound Notification Pipeline
            if alert:
                email_data = {
                    "subject": "Amazon India Price Drop Alert",
                    "message": f"The price of the article is below your set price of ₹{target_threshold} (Current price: ₹{price_as_float}). So hurry up!\n\nLink: {live_url}"
                }
                
                # Post data packet directly to the Formspree microservice via 'requests'
                post_response = requests.post(formspree_url, data=email_data)
                
                if post_response.status_code == 200:
                    print("Email successfully sent via Formspree!")
                else:
                    print(f"Failed to hand off mail packet. Formspree API Status: {post_response.status_code}")
            else:
                print(f"Price (₹{price_as_float}) is stable. No alert triggered for target threshold (₹{target_threshold}).")
                
        except ValueError:
            print(f"Data cleaning failed. String formatting '{clean_price_string}' incompatible with float initialization.")
    else:
        print("Could not find the price element. Amazon WAF layer may be serving a CAPTCHA challenge.")

finally:
    # The 'finally' block ensures that no matter what happens (even if the script crashes),
    # the browser window will be closed, freeing up your computer's memory.
    driver.quit()
