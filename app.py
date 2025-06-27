import streamlit as st
import pickle
import pandas as pd
import requests
import random
import gzip


@st.cache_data(show_spinner=False)
def fetch_poster(movie_id, delay=1):
    api_key = "52317e033dc3b1e931c65a266102c32c"
    api_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=52317e033dc3b1e931c65a266102c32c&language=en-US"
    
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        print(data)
        poster_path = data.get('poster_path')
        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/w185{poster_path}"
            return image_url
    except Exception as e:
        print(f"failed → {e}")

    # If all retries failed:
    fallback_url = "https://placehold.co/500x750?text=No+Poster"
    return fallback_url

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

movies_dict = pickle.load(open('./movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

with gzip.open('./similarity_compressed.pkl.gz', 'rb') as f:
  similarity = pickle.load(f)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a Movie',movies['title'].values)

if st.button('Recommend'):
  recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    st.text(recommended_movie_names[0])
    st.image(recommended_movie_posters[0])
  with col2:
    st.text(recommended_movie_names[1])
    st.image(recommended_movie_posters[1])
  with col3:
    st.text(recommended_movie_names[2])
    st.image(recommended_movie_posters[2])
  with col4:
    st.text(recommended_movie_names[3])
    st.image(recommended_movie_posters[3])
  with col5:
    st.text(recommended_movie_names[4])
    st.image(recommended_movie_posters[4])