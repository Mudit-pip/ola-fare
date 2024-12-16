from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pickle
import os
import time
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, request, jsonify
from threading import Thread

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

# Initialize the driver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")  # Run without GUI
    options.add_argument("--no-sandbox")  # Required in some environments
    options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues
    options.binary_location = "/usr/bin/google-chrome"  # Path to Chrome binary

    # Initialize the WebDriver with the correct paths
    driver = webdriver.Chrome(
        service=Service("/usr/local/bin/chromedriver"),  # Path to ChromeDriver
        options=options
    )
    return driver

# Load cookies if available
def load_cookies(driver, cookies_file):
    if os.path.exists(cookies_file):
        with open(cookies_file, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("Cookies loaded!")
    else:
        print("No cookies file found. Proceeding with manual login.")

# Log in using cookies or prompt for manual login
def login_ola(driver, cookies_file, lat_start, lng_start, lat_end, lng_end):
    driver.get(f"https://book.olacabs.com/?serviceType=p2p&utm_source=widget_on_olacabs&drop_lat={lat_end}&drop_lng={lng_end}&lat={lat_start}&lng={lng_start}")
    if os.path.exists(cookies_file):
        load_cookies(driver, cookies_file)
        driver.refresh()
        print("Logged in using saved cookies!")
        return True
    else:
        print("Cookies not found. Manual login required.")
        return False

# Get fares from the shadow DOM
def get_fares_from_shadow_dom(driver):
    try:
        ola_app = driver.find_element(By.CSS_SELECTOR, "ola-app.has-banner")
        ola_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_app)
        iron_pages = ola_shadow.find_element(By.CSS_SELECTOR, "iron-pages")
        ola_home = iron_pages.find_element(By.CSS_SELECTOR, "ola-home")
        ola_home_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_home)
        page_container = ola_home_shadow.find_element(By.CSS_SELECTOR, "div.page-container.bg-light")
        ola_home_local = page_container.find_element(By.CSS_SELECTOR, "ola-home-local")
        ola_home_local_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_home_local)
        cabs_list_section = ola_home_local_shadow.find_element(By.CSS_SELECTOR, "div.cabs-list-section")
        ola_cabs = cabs_list_section.find_element(By.CSS_SELECTOR, "ola-cabs")
        ola_cabs_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_cabs)
        cab_rows = ola_cabs_shadow.find_elements(By.CSS_SELECTOR, "div.row.cab-row.ptr.ola-ripple")
        fares = []
        for row in cab_rows:
            middle_div = row.find_element(By.CSS_SELECTOR, "div.middle")
            price_span = middle_div.find_element(By.CSS_SELECTOR, "span.text.value.price span")
            fare = price_span.text
            vehicle_span = middle_div.find_element(By.CSS_SELECTOR, "div.text.value.cab-name")
            vehicle_type = vehicle_span.text
            fares.append((fare, vehicle_type.split("\n")[0]))
        return fares
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Flask endpoint
@app.route('/run', methods=['GET'])
def run_selenium():
    lat_start = request.args.get('lat_start')
    lng_start = request.args.get('lng_start')
    lat_end = request.args.get('lat_end')
    lng_end = request.args.get('lng_end')

    if not all([lat_start, lng_start, lat_end, lng_end]):
        return jsonify({'error': 'Missing required query parameters'}), 400

    driver = init_driver()
    # login_ola(driver, "cookies.pkl", lat_start, lng_start, lat_end, lng_end)
    login_thread = Thread(target=login_ola, args=(driver, "cookies.pkl", lat_start, lng_start, lat_end, lng_end))
    login_thread.start()
    login_thread.join()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ola-app.has-banner")))
    time.sleep(0.5)

    fares = get_fares_from_shadow_dom(driver)
    driver.quit()
    return jsonify({'fares': fares})



if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0')
