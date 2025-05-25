
from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objs as go
import os
from scraper import scrape_and_save, get_trends

app = Flask(__name__)

def load_data():
    try:
        if not os.path.exists("data/jobs.csv") or os.path.getsize("data/jobs.csv") == 0:
            return pd.DataFrame()
        return pd.read_csv("data/jobs.csv")
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

@app.route("/")
def index():
    keyword = request.args.get("keyword", "software engineer")
    df = load_data()

    if df.empty:
        df = scrape_and_save(keyword)

    if df.empty:
        return "No data available. Try again later."

    trends = get_trends(df)

    title_chart = go.Figure([go.Bar(x=[t[0] for t in trends["top_titles"]],
                                    y=[t[1] for t in trends["top_titles"]])])
    skill_chart = go.Figure([go.Bar(x=[s[0] for s in trends["top_skills"]],
                                    y=[s[1] for s in trends["top_skills"]])])
    city_chart = go.Figure([go.Bar(x=[c[0] for c in trends["top_cities"]],
                                   y=[c[1] for c in trends["top_cities"]])])
    date_chart = go.Figure([go.Bar(x=[d[0] for d in trends["post_trend"]],
                                   y=[d[1] for d in trends["post_trend"]])])

    return render_template("index.html", title_chart=title_chart.to_html(full_html=False),
                           skill_chart=skill_chart.to_html(full_html=False),
                           city_chart=city_chart.to_html(full_html=False),
                           date_chart=date_chart.to_html(full_html=False),
                           keyword=keyword)

if __name__ == "__main__":
    app.run(debug=True)