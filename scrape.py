import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options  
from webdriver_manager.chrome import ChromeDriverManager  
import time
import streamlit as st # Import streamlit for error display

def scrape_website(website):
    print("Launching chrome browser...")

    # specifies how the web driver should operate (settings for it)
    options = Options()
    options.add_argument("--headless")  # Run headless (no GUI)
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("window-size=1920x1080") # Specify window size

    # sets up the Chrome webdriver
    # this is an application that allows us to control chrome
    # This now automatically downloads and uses the correct driver
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=options
        )
    except Exception as e:
        # Display an error in the Streamlit app if driver fails
        st.error(f"Error initializing Chrome driver: {e}")
        print(f"Error initializing Chrome driver: {e}")
        return None

    try:
        # uses webdriver to go to website
        driver.get(website) 

        print("Page loaded...")

        # gets the website's html
        html = driver.page_source 

        # Note: time.sleep() will freeze your Streamlit app. 
        # It's okay for simple scripts, but for complex waits,
        # you should use WebDriverWait.
        time.sleep(10) 

        return html
    except Exception as e:
        st.error(f"Error during scraping: {e}")
        print(f"Error during scraping: {e}")
        return None
    finally:
        # Ensure the driver is quit even if errors occur
        if 'driver' in locals() and driver:
            driver.quit()
            print("Chrome browser closed.")
