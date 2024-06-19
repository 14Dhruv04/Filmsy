import requests
import difflib
from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

app = Flask(__name__)

api_key = 'a15c794b'

def fetch_movie_data(movie_title):
    url = f'http://www.omdbapi.com/?apikey={api_key}&s={movie_title}'
    response = requests.get(url)
    data = response.json()
    return data.get('Search', [])

def fetch_movie_details(imdb_id):
    url = f'http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}'
    response = requests.get(url)
    data = response.json()
    return data

def get_movie_recommendations(movie_title):
    movies = fetch_movie_data(movie_title)

    if not movies:
        return []

    detailed_movies = []
    for movie in movies:
        movie_details = fetch_movie_details(movie['imdbID'])
        if 'Genre' in movie_details and 'Title' in movie_details:
            detailed_movies.append(movie_details)

    movies_data = pd.DataFrame(detailed_movies)
    movies_data['combined_features'] = movies_data['Title'] + ' ' + movies_data['Genre']
    vectorizer = TfidfVectorizer(stop_words='english')
    feature_vectors = vectorizer.fit_transform(movies_data['combined_features'])
    similarity = cosine_similarity(feature_vectors)
    list_of_all_titles = movies_data['Title'].tolist()
    find_close_match = difflib.get_close_matches(movie_title, list_of_all_titles)

    if not find_close_match:
        return []

    close_match = find_close_match[0]
    index_of_the_movie = movies_data[movies_data.Title == close_match].index[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommended_movies = []
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movies_data.iloc[index]['Title']
        poster_from_index = movies_data.iloc[index]['Poster']
        if title_from_index.lower() != movie_title.lower():
            recommended_movies.append({
                'title': title_from_index,
                'poster': poster_from_index
            })
        if len(recommended_movies) >= 30:
            break

    return recommended_movies

@app.route('/', methods=['GET', 'POST'])

def home():
    recommendations = []
    error = None
    if request.method == 'POST':
        movie_title = request.form['movie_title']
        recommendations = get_movie_recommendations(movie_title)
        if not recommendations:
            error = 'No similar movies found. Please try another movie title.'

    return render_template('index.html', recommendations=recommendations, error=error)

if __name__ == '__main__':
    app.run(debug=True)
