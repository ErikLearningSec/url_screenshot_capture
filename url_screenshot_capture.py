import sys
import os
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def capture_screenshot(url, idx):
    try:
        chrome_service = Service(executable_path=r'C:\chromedriver.exe')

        cdriver = webdriver.ChromeOptions()
        cdriver.add_argument('--headless=new')
        driver = webdriver.Chrome(service=chrome_service, options=cdriver)
        driver.set_window_size(1920, 1200)
        driver.get(url)

        # Wait for the page to be fully loaded (you can adjust the timeout as needed)
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        screenshot_path = os.path.join(out_folder, f'screenshot_{idx+1}_{url.replace("://", "_").replace(".", "_")}.png')
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot {idx + 1} for URL '{url}' captured successfully and saved at: {screenshot_path}")

        return screenshot_path  # Return the path to the captured screenshot

    except Exception as e:
        print(f"Error occurred while capturing screenshot for URL '{url}': {str(e)}")
        return None

def generate_html(screenshot_paths):
    try:
        html_content = "<html><body>"
        for idx, path in enumerate(screenshot_paths):
            if path:
                # Extract URL from the filename
                url_from_filename = os.path.splitext(os.path.basename(path))[0].split("_", 3)[-1].replace("_", ".")
                html_content += f"<h1>Screenshot {idx + 1} for URL '{url_from_filename}'</h1><img src='{path}' alt='Screenshot {idx + 1}'><br>"

        html_content += "</body></html>"

        html_file_path = os.path.join(out_folder, 'screenshots.html')
        with open(html_file_path, 'w') as html_file:
            html_file.write(html_content)

        print(f"HTML file generated successfully: {html_file_path}")

    except Exception as e:
        print(f"Error occurred while generating HTML file: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the file containing the list of URLs as the first argument.")
        sys.exit(1)

    url_file = sys.argv[1]

    if not os.path.exists(url_file):
        print("URL file does not exist.")
        sys.exit(1)

    out_folder = os.path.join(os.path.dirname(url_file), 'screenshot_captured')
    os.makedirs(out_folder, exist_ok=True)

    screenshot_paths = []
    urls = []

    try:
        with open(url_file, 'r') as file:
            urls = file.readlines()
            urls = [url.strip() for url in urls]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_url = {executor.submit(capture_screenshot, url, idx): (url, idx) for idx, url in enumerate(urls)}
                for future in concurrent.futures.as_completed(future_to_url):
                    url, idx = future_to_url[future]
                    try:
                        screenshot_path = future.result()
                        screenshot_paths.append(screenshot_path)
                    except Exception as e:
                        print(f"URL '{url}' generated an exception: {str(e)}")

        # Generate HTML file after capturing all screenshots
        generate_html(screenshot_paths)

    except Exception as ex:
        print(f"An error occurred: {str(ex)}")
