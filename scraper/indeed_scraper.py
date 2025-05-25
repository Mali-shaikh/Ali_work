
import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_indeed(keyword="software engineer", location="Pakistan", max_pages=2):
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(0, max_pages * 10, 10):
        url = f"https://pk.indeed.com/jobs?q={keyword}&l={location}&start={page}"
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")

        for job_card in soup.find_all("div", class_="job_seen_beacon"):
            title = job_card.find("h2", class_="jobTitle")
            company = job_card.find("span", class_="companyName")
            location = job_card.find("div", class_="companyLocation")
            date = job_card.find("span", class_="date")

            jobs.append({
                "title": title.text.strip() if title else "",
                "company": company.text.strip() if company else "",
                "location": location.text.strip() if location else "",
                "skills": "",
                "date_posted": date.text.strip() if date else ""
            })

        time.sleep(random.uniform(1, 3))

    return jobs
