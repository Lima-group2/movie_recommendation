import streamlit as st

# 👇 MUST be first Streamlit command
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

import pickle
import pandas as pd
import os
import gdown
import joblib
import requests

# ---------------- Load Pickled Data ----------------
@st.cache_resource
def load_data():


# 1️⃣ Define the helper function first
    def download_from_drive(file_id, destination):
        print(f"Downloading to {destination}...")
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {destination}")
    else:
        print(f"Failed to download {destination}. Status Code: {response.status_code}")

# 2️⃣ Then define load_data() afterwards
def load_data():
    os.makedirs('artifacts', exist_ok=True)

    files = {
        'movie_list.pkl': '1hLZkkyIG3AbydS7sVXj_zTs5JorULjNJ',
        'similarity.pkl': '1jc_C9ocFfnnwECaJ9L3gHEGbSIPr7d8x'
    }

    for filename, file_id in files.items():
        filepath = os.path.join('artifacts', filename)
        if not os.path.exists(filepath):
            download_from_drive(file_id, filepath)

    movies = pickle.load(open(os.path.join('artifacts', 'movie_list.pkl'), 'rb'))
    similarity = pickle.load(open(os.path.join('artifacts', 'similarity.pkl'), 'rb'))

    return movies, similarity


# --- Sidebar ---
with st.sidebar:
    st.image("images/logo.PNG", use_container_width=True)
    st.title("🎥 Recommender")
    st.markdown("Created by: *LIMA-2 ML & AI*")
    st.markdown("---")
    st.write("Select a movie to get content-based recommendations based on cast, crew, and keywords.")

# ---------------- Recommendation Logic ----------------
def recommend(movie):
    if movie not in movies['title'].values:
        return []
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]
    recommended_titles = [movies.iloc[i[0]].title for i in distances]
    return recommended_titles

# ---------------- Main App UI ----------------
st.title("🎬 Movie Recommender System")
st.markdown("Select a movie and discover similar recommendations powered by NLP and cosine similarity.")

selected_movie = st.selectbox("🎞️ Choose a movie:", movies['title'].values)

if st.button("🚀 Recommend"):
    recommendations = recommend(selected_movie)
    if recommendations:
        st.subheader("🎯 Top Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
    else:
        st.warning("Movie not found or no recommendations available.")
