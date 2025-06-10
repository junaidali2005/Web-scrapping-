import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL
base_url = "http://quotes.toscrape.com"
page_url = "/"

# Store data
all_quotes = []

while page_url:
    print(f"Scraping {base_url + page_url}")
    response = requests.get(base_url + page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    quotes = soup.find_all("div", class_="quote")
    
    for quote in quotes:
        text = quote.find("span", class_="text").text.strip()
        author = quote.find("small", class_="author").text.strip()
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]
        
        all_quotes.append({
            "Quote": text,
            "Author": author,
            "Tags": ", ".join(tags)
        })
    
    # Check for "Next" button
    next_btn = soup.find("li", class_="next")
    page_url = next_btn.a["href"] if next_btn else None

    # Optional: slow down scraping
    time.sleep(1)

# Save data
df = pd.DataFrame(all_quotes)
df.to_csv("quotes_full_scrape.csv", index=False, encoding="utf-8")
print("✅ Scraping Complete! Data saved to 'quotes_full_scrape.csv'")
