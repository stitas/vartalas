import time
import random
import argparse
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to read URLs from a file
def read_urls_from_file(file_path):
    """
    Reads a list of URLs from a text file, ignoring blank lines and comments.
    :param file_path: Path to the file containing URLs
    :return: List of URL strings
    """
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
# First 4 scroll actions are downward, remaining scrolls are upward
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
        # Determine scroll chunk size
        chunk = random.randint(100, int(page_height * 0.2))
        # First 4 scrolls go down, then scrolls go up
        direction = 1 if scroll_count < 6 else random.choice([1, -1])
        target = max(0, min(page_height, current_pos + direction * chunk))
        distance = target - current_pos

        # Break the distance into small, smooth steps
        step_size = random.randint(min_step, max_step)
        steps = max(1, int(abs(distance) / step_size))
        for _ in range(steps):
            driver.execute_script("window.scrollBy(0, arguments[0]);", distance / steps)
            time.sleep(random.uniform(min_step_delay, max_step_delay))

        current_pos = target
        scroll_count += 1
        # Pause briefly before next chunk
        time.sleep(random.uniform(min_wait, max_wait))


def main(urls_file):
    # Read URLs from file
    urls = read_urls_from_file(urls_file)
    if not urls:
        print("No URLs to visit. Please check the file path.")
        return

    options = uc.ChromeOptions()
    options.add_argument("--disable-features=HttpsUpgrades")
    driver = uc.Chrome(options=options)

    try:
        for url in urls:
            print(f"Visiting: {url}")
            driver.get(url, )

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
        print(f"Error visiting {url}: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Randomly scroll a list of URLs from a file")
    parser.add_argument('urls_file', help='Path to the text file containing URLs')
    args = parser.parse_args()
    main(args.urls_file)
