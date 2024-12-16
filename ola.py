# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# import pickle
# import os
# import time

# # Initialize the driver
# def init_driver():
#     options = Options()
#     options.add_argument("--disable-notifications")
#     service = Service(executable_path="chromedriver.exe")
#     driver = webdriver.Chrome(service=service, options=options)
#     return driver

# # Load cookies if available
# def load_cookies(driver, cookies_file):
#     if os.path.exists(cookies_file):
#         with open(cookies_file, "rb") as file:
#             cookies = pickle.load(file)
#             for cookie in cookies:
#                 driver.add_cookie(cookie)
#         print("Cookies loaded!")
#     else:
#         print("No cookies file found. Proceeding with manual login.")

# # Save cookies after manual login
# def save_cookies(driver, cookies_file):
#     with open(cookies_file, "wb") as file:
#         pickle.dump(driver.get_cookies(), file)
#     print("Cookies saved!")

# # Log in using cookies or prompt for manual login
# def login_ola(driver, cookies_file):
#     driver.get("https://book.olacabs.com/?serviceType=p2p&utm_source=widget_on_olacabs&drop_lat=26.89487&drop_lng=75.81065&lat=26.87404&lng=75.78909")

#     # Try to use cookies
#     if os.path.exists(cookies_file):
#         load_cookies(driver, cookies_file)
#         driver.refresh()
        
#         # Wait for the page to refresh and check if still on login page
#         try:
#             WebDriverWait(driver, 10).until(EC.url_changes)
#             if "login" in driver.current_url.lower():
#                 print("Cookies expired or invalid. Manual login required.")
#             else:
#                 print("Logged in using saved cookies!")
#                 return  # Login successful
#         except:
#             print("Error in waiting for page refresh.")

#     else:
#         print("No cookies found. Manual login required.")
    
#     # Prompt manual login if cookies fail
#     print("Log in manually on the browser...")
#     input("Press Enter after logging in...")
#     save_cookies(driver, cookies_file)
#     print("Logged in manually and cookies saved.")



# # def get_fares_from_shadow_dom(driver):
# #     try:    
# #         # Access the outermost shadow DOM
# #         ola_app = driver.find_element(By.CSS_SELECTOR, "ola-app.has-banner")
# #         ola_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_app)

# #         # Navigate deeper into the shadow DOM hierarchy
# #         iron_pages = ola_shadow.find_element(By.CSS_SELECTOR, "iron-pages")
# #         ola_home = iron_pages.find_element(By.CSS_SELECTOR, "ola-home")
# #         ola_home_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_home)

# #         page_container = ola_home_shadow.find_element(By.CSS_SELECTOR, "div.page-container.bg-light")
# #         ola_home_local = page_container.find_element(By.CSS_SELECTOR, "ola-home-local")
# #         ola_home_local_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_home_local)

# #         cabs_list_section = ola_home_local_shadow.find_element(By.CSS_SELECTOR, "div.cabs-list-section")
# #         ola_cabs = cabs_list_section.find_element(By.CSS_SELECTOR, "ola-cabs")
# #         ola_cabs_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_cabs)

# #         # Get all the "row cab-row ptr ola-ripple" elements
# #         cab_rows = ola_cabs_shadow.find_elements(By.CSS_SELECTOR, "div.row.cab-row.ptr.ola-ripple")
# #         fares = []

# #         for row in cab_rows:
# #             # Navigate to the div with class="middle" inside each row
# #             middle_div = row.find_element(By.CSS_SELECTOR, "div.middle")
# #             # Get the span with class="text value price"
# #             price_span = middle_div.find_element(By.CSS_SELECTOR, "span.text.value.price span")
# #             fare = price_span.text
# #             fares.append(fare)
# #             print(f"Fare: {fare}")  # Print the fare

# #         return fares  # Return the list of fares for further use

# #     except Exception as e:
# #         print(f"An error occurred: {e}")
# #         return []

# def get_fares_from_shadow_dom(driver):
#     try:    
#         # Access the outermost shadow DOM
#         ola_app = driver.find_element(By.CSS_SELECTOR, "ola-app.has-banner")
#         ola_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_app)

#         # Navigate deeper into the shadow DOM hierarchy
#         iron_pages = ola_shadow.find_element(By.CSS_SELECTOR, "iron-pages")
#         ola_home = iron_pages.find_element(By.CSS_SELECTOR, "ola-home")
#         ola_home_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_home)

#         page_container = ola_home_shadow.find_element(By.CSS_SELECTOR, "div.page-container.bg-light")
#         ola_home_local = page_container.find_element(By.CSS_SELECTOR, "ola-home-local")
#         ola_home_local_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_home_local)

#         cabs_list_section = ola_home_local_shadow.find_element(By.CSS_SELECTOR, "div.cabs-list-section")
#         ola_cabs = cabs_list_section.find_element(By.CSS_SELECTOR, "ola-cabs")
#         ola_cabs_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_cabs)

#         # Get all the "row cab-row ptr ola-ripple" elements
#         cab_rows = ola_cabs_shadow.find_elements(By.CSS_SELECTOR, "div.row.cab-row.ptr.ola-ripple")
#         fares = []

#         for row in cab_rows:
#             # Navigate to the div with class="middle" inside each row
#             middle_div = row.find_element(By.CSS_SELECTOR, "div.middle")

#             # Get the span with class="text value price"
#             price_span = middle_div.find_element(By.CSS_SELECTOR, "span.text.value.price span")
#             fare = price_span.text

#             # Get the vehicle type
#             vehicle_span = middle_div.find_element(By.CSS_SELECTOR, "div.text.value.cab-name")
#             vehicle_type = vehicle_span.text

#             fares.append((fare, vehicle_type.split("\n")[0]))  # Store both fare and vehicle type as a tuple

#         return fares  # Return the list of (fare, vehicle_type) tuples for further use

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []




# # Main function
# def main():
#     cookies_file = "cookies.pkl"
#     driver = init_driver()
#     try:
#         login_ola(driver, cookies_file)
#         print("Ready to fetch data or perform actions...")
        
#         WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ola-app.has-banner")))
    
#         time.sleep(0.5)
#         fares = get_fares_from_shadow_dom(driver)
#         print("Extracted Fares:", fares)

#         # get_fare_details(driver)

#     finally:
#         # time.sleep(5)  # Keep browser open briefly for debugging
#         driver.quit()

# if __name__ == "__main__":
#     main()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pickle
import os
import time
from threading import Thread

# Initialize the driver
def init_driver():
    options = Options()
    options.add_argument("--disable-notifications")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
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

# Save cookies after manual login
def save_cookies(driver, cookies_file):
    with open(cookies_file, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("Cookies saved!")

# Log in using cookies or prompt for manual login
def login_ola(driver, cookies_file, lat_start, lng_start, lat_end, lng_end):
    # driver.get("https://book.olacabs.com/?serviceType=p2p&utm_source=widget_on_olacabs&drop_lat=26.89487&drop_lng=75.81065&lat=26.87404&lng=75.78909")
    driver.get(f"https://book.olacabs.com/?serviceType=p2p&utm_source=widget_on_olacabs&drop_lat={lat_start}&drop_lng={lng_start}&lat={lat_end}&lng={lng_end}")

    # Try to use cookies
    if os.path.exists(cookies_file):
        load_cookies(driver, cookies_file)
        driver.refresh()
        
        # Wait for the page to refresh and check if still on login page
        try:
            WebDriverWait(driver, 10).until(EC.url_changes)
            if "login" in driver.current_url.lower():
                print("Cookies expired or invalid. Manual login required.")
            else:
                print("Logged in using saved cookies!")
                return True  # Login successful
        except:
            print("Error in waiting for page refresh.")

    else:
        print("No cookies found. Manual login required.")
    
    # Prompt manual login if cookies fail
    print("Log in manually on the browser...")
    input("Press Enter after logging in...")
    save_cookies(driver, cookies_file)
    print("Logged in manually and cookies saved.")
    return True  # Manual login complete

# Get fares from the shadow DOM
def get_fares_from_shadow_dom(driver):
    try:    
        # Access the outermost shadow DOM
        ola_app = driver.find_element(By.CSS_SELECTOR, "ola-app.has-banner")
        ola_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_app)

        # Navigate deeper into the shadow DOM hierarchy
        iron_pages = ola_shadow.find_element(By.CSS_SELECTOR, "iron-pages")
        ola_home = iron_pages.find_element(By.CSS_SELECTOR, "ola-home")
        ola_home_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_home)

        page_container = ola_home_shadow.find_element(By.CSS_SELECTOR, "div.page-container.bg-light")
        ola_home_local = page_container.find_element(By.CSS_SELECTOR, "ola-home-local")
        ola_home_local_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_home_local)

        cabs_list_section = ola_home_local_shadow.find_element(By.CSS_SELECTOR, "div.cabs-list-section")
        ola_cabs = cabs_list_section.find_element(By.CSS_SELECTOR, "ola-cabs")
        ola_cabs_shadow = driver.execute_script("return arguments[0].shadowRoot", ola_cabs)

        # Get all the "row cab-row ptr ola-ripple" elements
        cab_rows = ola_cabs_shadow.find_elements(By.CSS_SELECTOR, "div.row.cab-row.ptr.ola-ripple")
        fares = []

        for row in cab_rows:
            # Navigate to the div with class="middle" inside each row
            middle_div = row.find_element(By.CSS_SELECTOR, "div.middle")

            # Get the span with class="text value price"
            price_span = middle_div.find_element(By.CSS_SELECTOR, "span.text.value.price span")
            fare = price_span.text

            # Get the vehicle type
            vehicle_span = middle_div.find_element(By.CSS_SELECTOR, "div.text.value.cab-name")
            vehicle_type = vehicle_span.text

            fares.append((fare, vehicle_type.split("\n")[0]))  # Store both fare and vehicle type as a tuple

        return fares  # Return the list of (fare, vehicle_type) tuples for further use

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Main function
def main():
    cookies_file = "cookies.pkl"
    driver = init_driver()

    # Start login process in a new thread
    login_thread = Thread(target=login_ola, args=(driver, cookies_file, 26.89623642831106, 75.82835899845071, 26.91528831869341, 75.81677493985184))
    login_thread.start()

    # Wait for the login process to complete
    login_thread.join()

    # Now proceed with getting fares
    # print("Ready to fetch data or perform actions...")

    # Wait a bit before calling the function to fetch fares
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ola-app.has-banner")))
    time.sleep(0.5)  # 0.5 seconds of wait time

    fares = get_fares_from_shadow_dom(driver)
    print("Extracted Fares:", fares)

    # input()
    driver.quit()

if __name__ == "__main__":
    main()
