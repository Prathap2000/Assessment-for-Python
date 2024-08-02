import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Companies list
companies = ["Google", "Microsoft", "Amazon", "Apple", "Facebook", "Netflix", "Salesforce", "IBM", "Intel", "Oracle"]

# LinkedIn Scraping using Selenium
def scrape_linkedin_jobs():
    all_job_listings = []
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    for company in companies:
        job_listings = []
        url = f"https://www.linkedin.com/jobs/search/?keywords={company}&geoId=92000000"
        driver.get(url)
        time.sleep(5)  # Increased wait time for page to load
        
        # Scroll down to load more jobs (if needed)
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(job_listings) < 10:
            # Locate job title elements
            job_elements = driver.find_elements(By.CSS_SELECTOR, 'a.base-card__full-link')
            print(f"Found {len(job_elements)} job elements on page.")
            for job in job_elements:
                if len(job_listings) >= 10:
                    break
                try:
                    # Extract job title from the <span> within the <a> tag
                    title_element = job.find_element(By.CSS_SELECTOR, 'span.sr-only')
                    title = title_element.text
                    job_listings.append({
                        "company": company,
                        "title": title
                    })
                except Exception as e:
                    print(f"Error extracting job title: {e}")
                    continue
            
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new jobs to load
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        all_job_listings.extend(job_listings)

    driver.quit()
    
    # Print the collected job titles for debugging
    print(f"Total job titles collected: {len(all_job_listings)}")
    
    return all_job_listings

# Save data to CSV
def save_to_csv(data, filename):
    if not data:
        print(f"No data to save in {filename}.")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Save data to JSON
def save_to_json(data, filename):
    with open(filename, 'w') as output_file:
        json.dump(data, output_file, indent=4)

# Main execution
if __name__ == "__main__":
    # Scrape LinkedIn jobs
    linkedin_jobs = scrape_linkedin_jobs()
    save_to_csv(linkedin_jobs, 'linkedin_jobs.csv')
    save_to_json(linkedin_jobs, 'linkedin_jobs.json')

    print("Data extraction and saving completed.")
