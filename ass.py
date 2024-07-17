from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
from bs4 import BeautifulSoup

# Path to your Chrome WebDriver executable
webdriver_path = "chromedriver.exe"

# Initialize the WebDriver with the specified path
service = Service(executable_path=webdriver_path)

start_time = time.time()

print("Starting WebDriver...")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

print("Navigating to the website...")
driver.get("https://hprera.nic.in/PublicDashboard")
driver.maximize_window()

# Wait for the projects to be visible
print("Waiting for projects to be visible...")
projects = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="reg-Projects"]/div/div/div')))
print("Projects are visible.")
print(f"Number of projects found: {len(projects)}")
# print("projects: ", projects)

results = []

# Limit to the number of projects available or the desired number (6), whichever is smaller
num_projects = min(6, len(projects))

for i in range(num_projects):
    print(f"Processing project {i+1}...")
    projects[i].find_element(By.CSS_SELECTOR, f'div:nth-child({i+1}) > div > div > a').click()

    # Wait for the project details to be visible
    print("Waiting for project details to be visible...")
    project_info = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#project-menu-html > div:nth-child(2) > div:nth-child(1) > div > table > tbody')))
    print("Project details are visible.")

    # Get the page source
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'lxml')

    # Find the table using CSS selector
    table = soup.select_one("#project-menu-html > div:nth-child(2) > div:nth-child(1) > div > table")

    # Specify the keywords for the first column
    keywords = ["GSTIN No.", "PAN No.", "Name", "Permanent Address"]

    project_data = []

    # Iterate through the rows of the table
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 0:
            first_column_text = cells[0].get_text(strip=True)
            if first_column_text in keywords:
                # Extract the data from the row as needed
                first_column_data = cells[0].get_text(strip=True)
                second_column_data = cells[1].find('span').get_text(strip=True) if cells[1].find('span') else cells[1].get_text(strip=True)
                row_data = [first_column_data, second_column_data]
                project_data.append(row_data)
                print(f"Extracted row data: {row_data}")  # Print the extracted row data immediately

    results.append(project_data)
    print(f"Finished processing project {i+1}.")

    # Close the info page
    print("Closing the project details page...")
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-data-display-tab_project_main > div > div > div.modal-footer.py-3 > button")))
    
    # Click the button
    button.click()
    print("Project details page closed.")
    
    # Re-fetch the projects list to ensure it's up-to-date
    projects = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="reg-Projects"]/div/div/div')))
    print(f"Number of projects after refresh: {len(projects)}")

# Close the driver
print("Quitting WebDriver...")
driver.quit()

# Print the results
print("Printing the results...")
for project in results:
    print(project)

print("Script completed.")