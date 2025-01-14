from time import sleep
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from datetime import datetime
import pytz
import os
import requests
from collections import Counter
from webdriver_manager.chrome import ChromeDriverManager
import html
from time import sleep
import json

API_KEY = "AIzaSyAtMfGtiG-F1wxqtuEXd-2XPsEO7JLycd4" # Added here for easy testing

# Google Translate API endpoint
TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"

# Function to translate text using Google Translate API
def translate_text(text, target_language="en"):
    # First decode any HTML entities before translating
    decoded_text = html.unescape(text)
    
    params = {
        "q": decoded_text,
        "target": target_language,
        "key": API_KEY
    }
    response = requests.post(TRANSLATE_URL, params=params)
    if response.status_code == 200:
        translated = response.json()["data"]["translations"][0]["translatedText"]
        
        # Decode any HTML entities in the translated text as well
        return html.unescape(translated)
    else:
        print(f"Translation API Error: {response.json()}")
        return decoded_text


# Function to scrape articles from EL PAIS and save details
def scrape_articles():
    # Set Chrome options to disable the automation banner and run in headless mode
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Needed for some environments like Codespaces
    chrome_options.add_argument("--disable-dev-shm-usage")  # Required for running in Docker containers

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the Opinion page
    driver.get("https://elpais.com/opinion/")

    # Prepare the file to save article details
    file_path = "article_details.txt"
    with open(file_path, 'w', encoding='utf-8') as file:
        # try:
        # Wait for the body to load and locate the main content section
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        body = driver.find_element(By.TAG_NAME, 'body')
        main_content = body.find_element(By.CSS_SELECTOR, 'main.mw.mw-mc')

        # Locate <article> elements inside the main content
        articles = WebDriverWait(main_content, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'article'))
        )

        # Get the top 5 articles
        top_5_articles = articles[:4]

        i = 1
        # Define the Madrid timezone
        madrid_tz = pytz.timezone('Europe/Madrid')
        madrid_current_date = datetime.now(madrid_tz).date()

        file.write(f'Top 5 Articles from EL PAIS: {madrid_current_date}\n\n')

        my_data = []

        # Process the top 5 articles
        for article in top_5_articles:
            # Use innerText to extract all nested text from the header
            header = article.find_element(By.TAG_NAME, 'h2').get_attribute('innerText') if article.find_element(By.TAG_NAME, 'header') else 'No header'
            translated_header = translate_text(header)  # Translate the header
            paragraph = article.find_element(By.TAG_NAME, 'p').get_attribute('innerText') if article.find_element(By.TAG_NAME, 'p') else 'No paragraph'

            # Handle figure/image extraction
            figure = article.find_element(By.TAG_NAME, 'figure') if article.find_elements(By.TAG_NAME, 'figure') else None
            figure_content = 'No Image Available for this Article'

            if figure:
                img = figure.find_element(By.TAG_NAME, 'img') if figure.find_elements(By.TAG_NAME, 'img') else None
                if img:
                    img_url = img.get_attribute('src')
                    figure_content = f"Image URL: {img_url}"
                    image_name = f"article_{i}_image.jpg"
                    image_path = os.path.join('downloaded_images', image_name)

                    if not os.path.exists('downloaded_images'):
                        os.makedirs('downloaded_images')

                    try:
                        img_data = requests.get(img_url).content
                        with open(image_path, 'wb') as img_file:
                            img_file.write(img_data)
                        figure_content += f"\nImage saved at {image_path}"
                    except Exception as e:
                        figure_content += f"\nFailed to download image: {e}"

            link = article.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")

            # Write article details to the file
            my_data.append([i, header, translated_header, figure_content, link])
            # file.write(f"Article {i}:\n")
            # file.write(f"Original Title: {header}\n")
            # file.write(f"Translated Title: {translated_header}\n")
            # file.write(f"Content: {paragraph}\n")
            # file.write(f"Image: {figure_content}\n\n")
            i += 1
        
        for data in my_data:
            link = data[4]
            driver.get(link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
            )
            content_element = driver.find_element(By.CSS_SELECTOR, '[data-dtm-region="articulo_cuerpo"]')
            paragraph = content_element.get_attribute('innerText')
            i = data[0]
            my_data[i-1].append(paragraph)

            file.write(f"Article {data[0]}:\n")
            file.write(f"Original Title: {data[1]}\n")
            file.write(f"Translated Title: {data[2]}\n")
            file.write(f"Content: {data[5]}\n")
            file.write(f"Image: {data[3]}\n\n")




        # except Exception as e:
        #     print(f"An error occurred while scraping articles: {e}") 
    executor_object = {
        'action': 'setSessionStatus',
        'arguments': {
            'status': "passed"
        }
    }
    browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
    driver.execute_script(browserstack_executor)

    # Close the browser
    driver.quit()

# Function to analyze repeated words in translated headers
def analyze_repeated_words(file_path):
    try:
        # Read the file to get translated headers
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        # Extract translated headers
        translated_headers = []
        for line in content:
            if line.startswith("Translated Title:"):
                header = line.split("Translated Title:", 1)[1].strip()
                translated_headers.append(header)

        # Analyze repeated words
        all_words = ' '.join(translated_headers).lower().split()
        word_counts = Counter(all_words)
        repeated_words = {word: count for word, count in word_counts.items() if count > 2}

        # Append repeated words analysis to the file
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write("\nRepeated Words in Translated Headers:\n")
            if repeated_words:
                for word, count in repeated_words.items():
                    file.write(f"{word}: {count}\n")
            else:
                file.write("No repeated words found.\n")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to execute the script
def main():
    # Scrap Top 5 Articles
    scrape_articles()
    
    # Analyze Repeated Words
    analyze_repeated_words("article_details.txt")

    # After scraping, read the file and print its contents
    with open("article_details.txt", 'r', encoding='utf-8') as file:
        file_content = file.read()
        print(file_content)

# Entry point for the script
if __name__ == "__main__":
    main()