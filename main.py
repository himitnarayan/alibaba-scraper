import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create data folder if not exists
os.makedirs("data", exist_ok=True)

# Setup driver
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

file = 0

for i in range(1, 100):
    url = f"https://sourcing.alibaba.com/rfq/rfq_search_list.htm?recently=Y&page={i}"
    print(f"🔎 Fetching page {i}...")

    driver.get(url)

    try:
        # Wait for RFQ cards to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".next-row.next-row-no-padding.alife-bc-brh-rfq-list__row")
            )
        )

        elems = driver.find_elements(By.CSS_SELECTOR, ".next-row.next-row-no-padding.alife-bc-brh-rfq-list__row")
        print(f"✅ {len(elems)} items found on page {i}")

        for elem in elems:
            html = elem.get_attribute("outerHTML")
            with open(f"data/{i}_{file}.html", "w", encoding="utf-8") as f:
                f.write(html)
            file += 1

    except Exception as e:
        print(f"❌ Error on page {i}: {e}")

    time.sleep(2)

driver.quit()
