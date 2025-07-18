from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

all_data = []

for file in os.listdir("data"):
    file_path = os.path.join("data", file)
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')
    rfq_items = soup.select(".brh-rfq-item")  # Multiple RFQs per page

    for item in rfq_items:
        try:
            # RFQ ID and Inquiry URL
            a_tag = item.select_one(".brh-rfq-item__subject-link")
            rfq_id = a_tag["href"].split("p=")[1].split("&")[0] if a_tag else "N/A"
            inquiry_url = "https:" + a_tag["href"] if a_tag else "N/A"
            title = a_tag["title"].strip() if a_tag else "N/A"

            # Buyer Name
            buyer_name = item.select_one(".text").text.strip()

            # Buyer Image or Initial
            img_tag = item.select_one(".img-con img")
            buyer_image = img_tag["src"] if img_tag else item.select_one(".default-img").text.strip()

            # Inquiry Time
            inquiry_time = item.select_one(".brh-rfq-item__publishtime")
            inquiry_time = inquiry_time.text.replace("Date Posted:", "").strip() if inquiry_time else "N/A"

            # Quotes Left
            quotes_left = item.select_one(".brh-rfq-item__quote-left span")
            quotes_left = quotes_left.text.strip() if quotes_left else "N/A"

            # Country
            country = item.select_one(".brh-rfq-item__country")
            country = country.text.replace("Posted in:", "").strip() if country else "N/A"

            # Quantity Required
            quantity = item.select_one(".brh-rfq-item__quantity-num")
            quantity = quantity.text.strip() if quantity else "N/A"

            # Email Confirmed
            email_confirmed = "Yes" if "Email Confirmed" in item.text else "No"

            # Placeholder fields (not found in HTML)
            complete_order = "N/A"
            typical_replies = "N/A"
            interactive_user = "N/A"

            # Dates
            inquiry_date = datetime.now().strftime("%Y-%m-%d")
            scraping_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Append extracted data
            all_data.append({
                "RFQ ID": rfq_id,
                "Title": title,
                "Buyer Name": buyer_name,
                "Buyer Image": buyer_image,
                "Inquiry Time": inquiry_time,
                "Quotes Left": quotes_left,
                "Country": country,
                "Quantity Required": quantity,
                "Email Confirmed": email_confirmed,
                "Complete Order via RFQ": complete_order,
                "Typical Replies": typical_replies,
                "Interactive User": interactive_user,
                "Inquiry URL": inquiry_url,
                "Inquiry Date": inquiry_date,
                "Scraping Date": scraping_date,
            })
        except Exception as e:
            print(f"⚠️ Error processing RFQ in {file}: {e}")

# Save to Excel
df = pd.DataFrame(all_data)
df.to_excel("alibaba_rfq_data.xlsx", index=False)

print("✅ All RFQs scraped and saved to 'alibaba_rfq_data.xlsx'")
