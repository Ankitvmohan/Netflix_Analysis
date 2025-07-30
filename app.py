import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="Netflix Data Analysis", layout="wide")

@st.cache_data

def load_data():
    data = pd.read_csv('netflix_1.csv')
    data.drop_duplicates(inplace=True)
    data.dropna(subset=['director', 'title', 'country'], inplace=True)
    data['date_added'] = pd.to_datetime(data['date_added'])
    data['year'] = data['date_added'].dt.year
    data['month'] = data['date_added'].dt.month
    return data

df = load_data()

# Sidebar
st.sidebar.header("Filter Content")
content_type = st.sidebar.multiselect("Select Content Type", options=df['type'].unique(), default=df['type'].unique())
years = st.sidebar.slider("Select Year Range", int(df['year'].min()), int(df['year'].max()), (2010, 2021))

filtered_df = df[(df['type'].isin(content_type)) & (df['year'].between(years[0], years[1]))]

# Main Page
st.title("\U0001F4FA Netflix Data Analysis & Visualization")
st.markdown("Explore content trends, genres, and ratings on Netflix.")

## Content Type Distribution
st.subheader("Distribution by Content Type")

type_counts = filtered_df['type'].value_counts()
st.bar_chart(type_counts)

# Create summary table for viewing and download
summary_df = filtered_df[["type", "title"]].groupby("type").count().reset_index()
summary_df = summary_df.rename(columns={"title": "Count"})
# Layout for expander and download
_, view1, dwn1 = st.columns([0.2, 0.45, 0.35])
with view1:
    with st.expander("📋 View Content Type Table"):
        st.write(summary_df)
with dwn1:
    csv_data = summary_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV", data=csv_data, file_name='content_type_distribution.csv', mime='text/csv')

## Ratings Distribution
st.subheader("Ratings Distribution")
rating_counts = filtered_df['rating'].value_counts()
st.bar_chart(rating_counts)

# Create summary DataFrame for table and download
summary_df_1 = filtered_df[['rating']].groupby('rating').size().reset_index(name='Count')

_, view2, dwn2 = st.columns([0.2, 0.45, 0.35])
with view2:
    with st.expander("📋 View Ratings Table"):
        st.write(summary_df_1)

with dwn2:
    csv_data = summary_df_1.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download CSV", data=csv_data, file_name='Ratings_Distribution.csv', mime='text/csv')

# Content Over Time
st.subheader("Content Added Over Time")
yearly_counts = filtered_df['year'].value_counts().sort_index()
st.line_chart(yearly_counts)

# Top Genres
st.subheader("Top Genres")
df['genres'] = df['listed_in'].str.split(', ')
all_genres = sum(df['genres'], [])
genre_counts = pd.Series(all_genres).value_counts().head(10)
st.bar_chart(genre_counts)

# Word Cloud
st.subheader("Word Cloud of Titles")
titles = " ".join(filtered_df['title'])
wordcloud = WordCloud(width=800, height=400, background_color='black').generate(titles)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

st.markdown("---")
st.caption("Built with \u2764\ufe0f using Streamlit")
