# 📉 Amazon Price Drop Alert Bot

An intelligent, fully automated web scraper built with Python and Selenium WebDriver. This bot monitors a specific product on Amazon India, bypasses bot-detection walls, cleans the data, and sends an email notification via the Formspree API if the price drops below your target threshold.

This project demonstrates advanced DOM interaction, data sanitization, API integration, and handling dynamic, JavaScript-heavy single-page applications.

## ✨ Key Features

* **Selenium WebDriver Engine:** Bypasses simple `requests/BeautifulSoup` blocks by acting as a real browser, naturally executing JavaScript, and waiting for dynamic pricing elements to load.
* **Robust Price Extraction:** Amazon frequently changes its UI layout. This bot uses a fallback hierarchy list to scan multiple CSS classes (`a-price-whole`, `a-offscreen`, `priceblock_ourprice`) ensuring it finds the price regardless of layout variations.
* **Intelligent Data Sanitization:** Automatically strips currency symbols (₹, $), commas, and trailing decimals, cleanly converting chaotic HTML text into a usable Python `float`.
* **API Mail Routing:** Uses the lightweight `requests` library to instantly post data to a Formspree webhook, firing an email to your inbox the moment the threshold is breached.

## 🛠️ Prerequisites

To run this script, you will need:
* **Python 3.7 or higher** installed.
* **Google Chrome** browser installed.
* A free [Formspree](https://formspree.io/) account (for email forwarding).

*(Note: Because this project uses Selenium 4, you do not need to manually download or configure a `chromedriver.exe`.)*

## 🚀 Installation & Configuration

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/amazon-price-alert-bot.git](https://github.com/YourUsername/amazon-price-alert-bot.git)
   cd amazon-price-alert-bot
   ```

2. **Install the required dependencies:**
   Run the following command in your terminal to install Selenium and Requests:
   ```bash
   pip install selenium requests
   ```

3. **Configure your targets:**
   Open `main.py` in your code editor and update the variables at the top of the file:
   * **`live_url`**: Paste the full Amazon URL of the product you want to track.
   * **`formspree_url`**: Paste your unique endpoint URL provided by Formspree.
   * **`target_threshold`**: Set the maximum price (as a float, e.g., `10000.00`). If the price drops below this number, the alert triggers.

## 🎮 How to Run

Execute the script from your terminal:

```bash
python main.py
```

*By default, the script will open a visible Chrome window so you can watch it work. If you plan to run this on a server or schedule it with cron/Task Scheduler, you can uncomment the `--headless=new` argument in the code to make it run invisibly in the background.*

## 🧠 Technical Highlights

* **User-Agent Spoofing:** To prevent Amazon's WAF (Web Application Firewall) from immediately serving a CAPTCHA, the Chrome options are injected with a highly specific, modern Windows 10 User-Agent string.
* **Targeted Text Content Extraction:** Uses `.get_attribute("textContent")` instead of standard `.text` to ensure the bot can read prices even if Amazon's CSS temporarily hides them from the screen (`a-offscreen`).

## ⚠️ Disclaimer

This script is meant for educational purposes. Web scraping high-traffic ecommerce sites should be done responsibly and infrequently. Check Amazon's Terms of Service regarding automated data collection.
