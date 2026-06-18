# AmzPriceMonitor (Amazon India Price Tracker)

An automated Python-based web scraping application designed to monitor product price fluctuations on Amazon India (`amazon.in`). The system cleanly parses unstructured HTML, sanitizes raw text data into structured types, and routes real-time price alerts to your inbox via a Formspree webhook endpoint.

## 🚀 Key Features

- **Multi-Selector Layout Cascade:** Resilient DOM parsing that traverses a fallback hierarchy (`a-price-whole`, `a-offscreen`, `priceblock_ourprice`) to handle variable Amazon UI layouts or A/B testing variations.
- **Robust Character Filtering Sanitizer:** Custom data sanitization loop that strips non-numeric artifacts (such as commas, whitespace, and currency symbols like ₹ or $) and converts raw text strings into accurate floats for relational math checks.
- **Header Impersonation Layer:** Implements a comprehensive production-grade browser request payload (including `Sec-Fetch-*` validation parameters) to mimic realistic user browser signatures and reduce Web Application Firewall (WAF) challenges.
- **Decoupled Notification Architecture:** Leverages a clean outbound HTTP POST request to offload email routing to a Formspree microservice, bypassing the overhead of direct SMTP handling or hardcoded authentication secrets.

## 🛠️ Tech Stack & Requirements

- **Language:** Python 3.8+
- **Libraries:** - `requests` (HTTP client)
  - `beautifulsoup4` (HTML extraction and tree parsing)

## 📋 Installation & Local Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/yourusername/amazon-price-tracker.git](https://github.com/yourusername/amazon-price-tracker.git)
   cd amazon-price-tracker
