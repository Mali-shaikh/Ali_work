
import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_rozee(keyword="software engineer", max_pages=2):
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, max_pages + 1):
        url = f"https://www.rozee.pk/job/jsearch/q/{keyword}/page/{page}"
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")

        for job_card in soup.find_all("div", class_="job_search_list"):
            title_tag = job_card.find("a", class_="job_title")
            company = job_card.find("span", class_="company_name")
            location = job_card.find("span", class_="job-location")
            date = job_card.find("span", class_="job-posted-date")

            jobs.append({
                "title": title_tag.text.strip() if title_tag else "",
                "company": company.text.strip() if company else "",
                "location": location.text.strip() if location else "",
                "skills": "",
                "date_posted": date.text.strip() if date else ""
            })

        time.sleep(random.uniform(1, 3))

    return jobs
