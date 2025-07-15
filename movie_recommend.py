import streamlit as st

# 👇 MUST be first Streamlit command
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

import pickle
import pandas as pd
import os

# ---------------- Load Pickled Data ----------------
import streamlit as st

import pickle
import joblib
import gdown
import os

import os
import joblib
import gdown
import streamlit as st

@st.cache_data
def load_data():
    os.makedirs("artifacts", exist_ok=True)

    movie_file = "artifacts/movie_list_compressed.joblib"
    similarity_file = "artifacts/similarity_compressed.joblib"

    movie_file_id = "1p_Y0LjDV8stiUaNsDZvzECJ6rydgt4yR"
    similarity_file_id = "1r0wkZNpof7LB_7H7cI792dDG-nGrkC_A"

    movie_url = f"https://drive.google.com/uc?id={movie_file_id}"
    similarity_url = f"https://drive.google.com/uc?id={similarity_file_id}"

    with st.spinner("📥 Downloading movie file..."):
        if not os.path.exists(movie_file):
            result = gdown.download(movie_url, movie_file, quiet=False, fuzzy=True)
            if result is None or not os.path.exists(movie_file):
                st.error("❌ Failed to download movie file.")
                st.stop()
        else:
            st.success("✅ Movie file ready.")

    with st.spinner("📥 Downloading similarity file..."):
        if not os.path.exists(similarity_file):
            result = gdown.download(similarity_url, similarity_file, quiet=False, fuzzy=True)
            if result is None or not os.path.exists(similarity_file):
                st.error("❌ Failed to download similarity file.")
                st.stop()
        else:
            st.success("✅ Similarity file ready.")

    try:
        movies = joblib.load(movie_file)
    except Exception as e:
        st.error(f"❌ Could not load movie file: {e}")
        st.stop()

    try:
        similarity = joblib.load(similarity_file)
    except Exception as e:
        st.error(f"❌ Could not load similarity file: {e}")
        st.stop()

    return movies, similarity


# --- Sidebar ---
with st.sidebar:
    st.image("images/logo.png", use_container_width=True)
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
movies, similarity = load_data()
selected_movie = st.selectbox("🎞️ Choose a movie:", movies['title'].values)

if st.button("🚀 Recommend"):
    recommendations = recommend(selected_movie)
    if recommendations:
        st.subheader("🎯 Top Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
    else:
        st.warning("Movie not found or no recommendations available.")
