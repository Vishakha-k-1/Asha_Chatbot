from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def fetch_herkey_programs():
    url = "https://www.herkey.com/groups"
    
    # Set up headless Chrome options
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU for headless
    options.add_argument('--no-sandbox')  # Disable sandboxing
    
    # Use ChromeDriver with headless mode
    driver = webdriver.Chrome(executable_path="path/to/chromedriver", options=options)
    
    driver.get(url)
    
    # Wait for dynamic content to load
    time.sleep(5)
    
    # Parse the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()  # Close the browser after scraping
    
    # Example logic to find mentorship programs
    mentorships = []
    sections = soup.find_all("section")
    for section in sections:
        title = section.get_text(strip=True)
        if "Mentor" in title or "Program" in title:
            mentorships.append({"name": title, "expertise": "Mentorship/Program"})
    
    return mentorships
