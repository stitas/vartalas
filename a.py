import time
import random
import argparse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService  

# Function to read URLs from a file
def read_urls_from_file(file_path):
    urls = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                urls.append(line)
    except FileNotFoundError:
        print(f"URL file not found: {file_path}")
    return urls

# Function to perform smooth, human-like scrolling
def human_like_scroll(driver, min_duration=10, max_duration=20,
                      min_wait=0.5, max_wait=2,
                      min_step=5, max_step=20,
                      min_step_delay=0.01, max_step_delay=0.03):
    duration = random.uniform(min_duration, max_duration)
    end_time = time.time() + duration
    page_height = driver.execute_script("return document.body.scrollHeight;")
    current_pos = driver.execute_script("return window.pageYOffset;")

    scroll_count = 0
    while time.time() < end_time:
        chunk = random.randint(100, int(page_height * 0.2))
        direction = 1 if scroll_count < 6 else random.choice([1, -1])
        target = max(0, min(page_height, current_pos + direction * chunk))
        distance = target - current_pos

        step_size = random.randint(min_step, max_step)
        steps = max(1, int(abs(distance) / step_size))
        for _ in range(steps):
            driver.execute_script("window.scrollBy(0, arguments[0]);", distance / steps)
            time.sleep(random.uniform(min_step_delay, max_step_delay))

        current_pos = target
        scroll_count += 1
        time.sleep(random.uniform(min_wait, max_wait))

# Create a WebDriver based on browser name
def get_driver(browser_name):
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

def main(urls_file, browser):
    urls = read_urls_from_file(urls_file)
    if not urls:
        print("No URLs to visit. Please check the file path.")
        return

    driver = get_driver(browser)

    try:
        for url in urls:
            print(f"Visiting: {url}")
            driver.get(url)

            # Click consent button if present
            try:
                consent_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-cta-consent"))
                )
                consent_btn.click()
                print("Clicked consent button.")
            except Exception:
                pass

            human_like_scroll(driver)
            time.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Randomly scroll a list of URLs using a selected browser")
    parser.add_argument("urls_file", help="Path to the text file containing URLs")
    parser.add_argument("--browser", choices=["chrome", "firefox", "edge"], default="chrome",
                        help="Browser to use (default: chrome)")
    args = parser.parse_args()
    main(args.urls_file, args.browser)
