import csv
import json
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to set up Selenium WebDriver with rotating user agents
def setup_driver():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    ]
    options = Options()
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    driver = webdriver.Chrome(options=options)
    return driver

# Function to simulate human-like delays
def human_delay():
    time.sleep(random.uniform(2, 5))

# Function to extract salary data for a specific role
def get_salary_data_for_role(role):
    url = f"https://www.ambitionbox.com/search?q={role.replace(' ', '%20')}"
    driver = setup_driver()
    driver.get(url)
    human_delay()

    salary_data = []

    try:
        # Wait until salary elements are present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".gs-bidi-start-align.gs-snippet"))
        )

        salary_elements = driver.find_elements(By.CSS_SELECTOR, ".gs-bidi-start-align.gs-snippet")
        if not salary_elements:
            print(f"No salary elements found for {role}. Check selectors.")
        
        for salary_element in salary_elements:
            text = salary_element.text

            # Extract average salary and salary range
            if "ranges between" in text and "with an average annual salary of" in text:
                parts = text.split("with an average annual salary of")
                
                if len(parts) == 2:
                    range_part = parts[0].split("ranges between")[1].strip()
                    average_salary_part = parts[1].split("Salary estimates")[0].strip()  # Remove extra context
                    
                    # Clean up the text
                    average_salary_part = average_salary_part.replace("₹", "").strip()
                    range_part = range_part.replace("₹", "").strip()
                    
                    # Append the cleaned data
                    salary_data.append({
                        "role": role,
                        "average_salary": f"₹ {average_salary_part}",
                        "salary_range": f"₹ {range_part}"
                    })
                # Stop after getting the first valid entry
                if salary_data:
                    break

    except Exception as e:
        print(f"Failed to fetch salary data for {role}: {e}")

    driver.quit()
    return salary_data

# Function to save data in CSV format
def save_data_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Function to save data in JSON format
def save_data_to_json(data, filename):
    if not data:
        print("No data to save.")
        return
    with open(filename, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=4, ensure_ascii=False)

# Main Function
def main():
    roles = ["Software Engineer", "Data Analyst", "Product Manager", "UX Designer", "Marketing Manager"]
    all_salary_data = []

    for role in roles:
        print(f"Fetching data for role: {role}")
        salary_data = get_salary_data_for_role(role)
        all_salary_data.extend(salary_data)

    # Save data to CSV and JSON
    save_data_to_csv(all_salary_data, 'ambition_box_salary_data.csv')
    save_data_to_json(all_salary_data, 'ambition_box_salary_data.json')

if __name__ == "__main__":
    main()
