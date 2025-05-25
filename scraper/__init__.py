
import pandas as pd
import os

def extract_skills(title):
    return title.lower().split()

def scrape_and_save(keyword="software engineer"):
    all_jobs = [{
        "title": "Software Engineer",
        "company": "Tech Co",
        "location": "New York",
        "skills": "",
        "date": "2024-05-20"
    }]

    for job in all_jobs:
        job["skills"] = extract_skills(job["title"])

    df = pd.DataFrame(all_jobs)
    df.drop_duplicates(inplace=True)

    if not os.path.exists("data"):
        os.makedirs("data")

    if not df.empty:
        df.to_csv("data/jobs.csv", index=False)

    return df

def get_trends(df):
    from collections import Counter

    # Normalize skills column
    def parse_skills(entry):
        if isinstance(entry, list):
            return [str(s).strip().lower() for s in entry if isinstance(s, str)]
        elif isinstance(entry, str):
            return [s.strip().lower() for s in entry.replace(",", " ").split()]
        return []

    df["skills"] = df["skills"].apply(parse_skills)

    all_skills = []
    for skill_list in df["skills"]:
        if isinstance(skill_list, list):
            all_skills.extend(skill_list)
    skill_count = Counter(all_skills).most_common(5)
    title_count = Counter(map(str, df["title"])).most_common(5)
    city_count = Counter(map(str, df["location"])).most_common(5)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        date_count = df["date"].dt.date.value_counts().sort_index()
        date_trend = list(zip(date_count.index.astype(str), date_count.values))
    else:
        date_trend = []

    return {
        "top_titles": title_count,
        "top_skills": skill_count,
        "top_cities": city_count,
        "post_trend": date_trend
    }



