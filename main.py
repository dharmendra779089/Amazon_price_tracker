import requests
from bs4 import BeautifulSoup

# 1. Setup your URLs and Headers
# Configured for Amazon India (.in)
live_url = "https://www.amazon.in/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
formspree_url = "https://formspree.io/f/your_form_id_here" 

# Upgraded header payload mimicking a production Google Chrome browser session
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1"
}

# 2. Fetch and Parse the Amazon Page
response = requests.get(live_url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Target fallback hierarchy to find the price element across varying Amazon UI layouts
price_element = soup.find(class_="a-price-whole")
if not price_element:
    price_element = soup.find(class_="a-offscreen")
if not price_element:
    price_element = soup.find("span", {"id": "priceblock_ourprice"})

# Verify an element was matched before executing string manipulations
if price_element:
    raw_price = price_element.get_text()
    
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
            
            # Post data packet directly to the Formspree microservice
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
    print("Could not find the price element. Amazon WAF layer may be serving a structural CAPTCHA challenge.")