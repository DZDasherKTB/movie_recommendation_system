import streamlit as st
import pickle
import pandas as pd
import requests
import random
import gzip

st.set_page_config(page_title="Movie Recommender", layout="wide")

# ======= CSS Styling for Responsiveness & Cards =======
st.markdown("""
<style>
/* Center title */
h1 {
    text-align: center;
    margin-top: 2rem;
}

/* Movie card hover effect */
.movie-card {
    text-align: center;
    transition: transform 0.3s ease;
}
.movie-card:hover {
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# ======= Poster Fetching =======
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    api_key = "52317e033dc3b1e931c65a266102c32c"
    api_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w185{poster_path}"  # ✅ your original size
    except Exception as e:
        print(f"failed → {e}")

    return "https://placehold.co/500x750?text=No+Poster"

# ======= Recommend Logic =======
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    selected = random.sample(movies_list, 5)

    recommended_movies = []
    recommended_movies_posters = []
    for i in selected:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movies_posters

# ======= Load Data =======
movies_dict = pickle.load(open('./movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
with gzip.open('./similarity_compressed.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

# ======= UI =======
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox("Select a movie to get recommendations", movies['title'].values)

if st.button('🔍 Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div class="movie-card">
                <h4>{names[idx]}</h4>
                <img src="{posters[idx]}" style="width:100%; border-radius: 10px;" />
            </div>
            """, unsafe_allow_html=True)

# ======= Portfolio Footer =======
st.markdown("""
<hr style="margin-top: 4rem;"/>
<p style="text-align:center; color: gray;">
    💡 Created by <a href="https://portfolio-theta-seven-36.vercel.app/#contact" target="_blank" style="color: #4ade80;">Dash</a>
</p>
""", unsafe_allow_html=True)
