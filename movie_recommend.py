import streamlit as st

# 👇 MUST be first Streamlit command
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

import pickle
import pandas as pd
import os

# ---------------- Load Pickled Data ----------------
@st.cache_resource
def load_data():
    movies = pickle.load(open("artifacts/movie_list.pkl", "rb"))
    similarity = pickle.load(open("artifacts/similarity.pkl", "rb"))
    return movies, similarity

movies, similarity = load_data()

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
