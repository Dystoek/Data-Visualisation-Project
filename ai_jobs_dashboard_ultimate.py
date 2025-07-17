
import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="AI Jobs Analytics", layout="wide", page_icon="🤖")

@st.cache_data
def load_data():
    df = pd.read_csv("ai_job_dataset_cleaned.csv")
    df['posting_date'] = pd.to_datetime(df['posting_date'])
    df['application_deadline'] = pd.to_datetime(df['application_deadline'])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("🔎 Filters")
locations = st.sidebar.multiselect("Company Location", df["company_location"].unique())
experience = st.sidebar.multiselect("Experience Level", df["experience_level"].unique())
education = st.sidebar.multiselect("Education Required", df["education_required"].unique())

filtered = df.copy()
if locations:
    filtered = filtered[filtered["company_location"].isin(locations)]
if experience:
    filtered = filtered[filtered["experience_level"].isin(experience)]
if education:
    filtered = filtered[filtered["education_required"].isin(education)]

# Header
st.title("🤖 AI Job Market Explorer - Pratik Rughe - Final Project")
st.markdown("Explore the AI job market using 20+ visual insights. Use the sidebar to filter the data.")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", len(filtered))
col2.metric("Avg Salary (USD)", f"${int(filtered['salary_usd'].mean()):,}")
col3.metric("Avg Experience (Yrs)", f"{filtered['years_experience'].mean():.1f}")
col4.metric("Remote Jobs (%)", f"{(filtered['remote_ratio'] == 100).mean() * 100:.1f}%")

st.markdown("---")

# Section 1: Job Titles
st.subheader("📌 Most Common AI Job Titles")
fig_titles = px.bar(filtered['job_title'].value_counts().nlargest(10), title="Top Job Titles")
st.plotly_chart(fig_titles, use_container_width=True)

# Section 2: Salary by Country
st.subheader("🌍 Average Salary by Country")
country_salary = filtered.groupby("company_location")["salary_usd"].mean().sort_values(ascending=False).head(10)
fig_salary_country = px.bar(country_salary, title="Top Countries by Average Salary", labels={"value":"Avg Salary", "index":"Country"})
st.plotly_chart(fig_salary_country, use_container_width=True)

# Section 3: Experience vs Salary
st.subheader("📈 Salary vs. Experience Level")
fig_exp_salary = px.box(filtered, x="experience_level", y="salary_usd", color="experience_level")
st.plotly_chart(fig_exp_salary, use_container_width=True)

# Section 4: Education vs Salary
st.subheader("🎓 Education vs. Salary")
fig_edu_salary = px.box(filtered, x="education_required", y="salary_usd", color="education_required")
st.plotly_chart(fig_edu_salary, use_container_width=True)

# Section 5: Industry Breakdown
st.subheader("🏢 Top Industries Hiring AI Talent")
fig_industry = px.bar(filtered["industry"].value_counts().nlargest(10), title="Top Industries")
st.plotly_chart(fig_industry, use_container_width=True)

# Section 6: Remote Work Distribution
st.subheader("🏠 Remote Work Distribution")
fig_remote = px.histogram(filtered, x="remote_ratio", nbins=10)
st.plotly_chart(fig_remote, use_container_width=True)

# Section 7: Word Cloud - Skills
st.subheader("💡 In-Demand Skills Word Cloud")
all_skills = ",".join(filtered["required_skills"].dropna().tolist())
wordcloud = WordCloud(width=1200, height=500, background_color='white').generate(all_skills)
fig, ax = plt.subplots(figsize=(15, 6))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Section 8: Global Job Map
st.subheader("🗺️ Global Job Distribution Map")
country_counts = filtered['company_location'].value_counts().reset_index()
country_counts.columns = ['country', 'count']
map_center = [20, 0]
m = folium.Map(location=map_center, zoom_start=2)
mc = MarkerCluster().add_to(m)
for idx, row in country_counts.iterrows():
    folium.Marker(location=[0, 0], popup=f"{row['country']}: {row['count']} jobs").add_to(mc)
folium_static(m)

# Section 9: Timeline of Job Postings
st.subheader("📅 Timeline of Job Postings")
timeline = filtered['posting_date'].value_counts().sort_index()
fig_timeline = px.line(x=timeline.index, y=timeline.values, labels={"x":"Date", "y":"Jobs"})
st.plotly_chart(fig_timeline, use_container_width=True)

# Section 10: Bubble Chart - Salary vs Experience vs Company Size
st.subheader("🔮 Salary vs Experience vs Job Length")
fig_bubble = px.scatter(filtered, x="years_experience", y="salary_usd",
                        size="job_description_length", color="company_size")
st.plotly_chart(fig_bubble, use_container_width=True)

# Footer
st.markdown("---")
st.caption("👨‍💻 Created by Pratik | Final Project | Data Visualisation | Summer 2025")
