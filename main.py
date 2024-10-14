import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

logging.basicConfig(filename='job_tracking.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

LOGIN_URL = "https://www.linkedin.com/login"
JOBS_URL = "https://www.linkedin.com/jobs/search/?currentJobId=4033360804&f_AL=true&keywords=python%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"

def login():
    driver.get(url=LOGIN_URL)

    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Accept Cookies"]'))
        )
        cookie_button.click()
        logging.info("Cookie acceptance button clicked.")
    except Exception as e:
        logging.error(f"Error finding cookie acceptance button: {e}")

    try:
        driver.find_element(By.ID, "username").send_keys(config.LINKEDIN_EMAIL)
        driver.find_element(By.ID, "password").send_keys(config.LINKEDIN_PASS)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        logging.info("Logged in successfully.")
    except Exception as e:
        logging.error(f"Error during login: {e}")

def get_job_urls():
    driver.get(url=JOBS_URL)
    time.sleep(2)
    jobs = driver.find_elements(By.CLASS_NAME, "job-card-container__link")
    job_url_list = []
    for job in jobs:
        job_url = job.get_attribute("href")
        if "www.linkedin.com/jobs/view/" in job_url and job_url not in job_url_list:
            job_url_list.append(job_url)
    logging.info(f"Found {len(job_url_list)} job URLs.")
    return job_url_list

def follow_company(job_link):
    driver.get(url=job_link)
    time.sleep(2)
    logging.info(f"Trying to follow the company for job link: {job_link}")

    try:
        company_link = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a[aria-label*='Company']"))
        )
        company_link.click()
        logging.info("Navigated to company page.")

        time.sleep(2)

        follow_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-control-name='follow']"))
        )
        follow_button.click()
        logging.info("Successfully followed the company.")
    except Exception as e:
        logging.error(f"Error following company: {e}")

def send_notification(job_link):
    print(f"Followed company for job: {job_link}")

def search_jobs_by_location(location):
    search_url = f"https://www.linkedin.com/jobs/search/?keywords=python%20developer&location={location}"
    driver.get(search_url)
    time.sleep(2)
    logging.info(f"Searched jobs in location: {location}")

def filter_by_experience_level(level):
    driver.find_element(By.CSS_SELECTOR, f"input[value='{level}']").click()
    time.sleep(2)
    logging.info(f"Filtered jobs by experience level: {level}")

def apply_to_job(job_link):
    driver.get(job_link)
    time.sleep(2)
    try:
        apply_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-control-name='apply_now']"))
        )
        apply_button.click()
        logging.info("Job application started.")
    except Exception as e:
        logging.error(f"Error applying to job: {e}")

def save_job(job_link):
    driver.get(job_link)
    time.sleep(2)
    try:
        save_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-control-name='save']"))
        )
        save_button.click()
        logging.info("Job saved successfully.")
    except Exception as e:
        logging.error(f"Error saving job: {e}")

def view_company_profile(job_link):
    driver.get(job_link)
    time.sleep(2)
    try:
        company_profile = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a[aria-label*='Company Profile']"))
        )
        company_profile.click()
        logging.info("Navigated to company profile.")
    except Exception as e:
        logging.error(f"Error viewing company profile: {e}")

driver = webdriver.Chrome()

login()
time.sleep(3)

url_list = get_job_urls()
if len(url_list) == 0:
    logging.warning("No jobs found. Ensure you're logged in properly or tweak the position or location name.")

for url in url_list:
    follow_company(url)
    send_notification(url)
    time.sleep(5)

search_jobs_by_location("New York")
filter_by_experience_level("entry_level")

for url in url_list:
    apply_to_job(url)
    time.sleep(2)

save_job(url_list[0])

view_company_profile(url_list[1])

driver.quit()
