import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Dataset Loader
def load_movies(path = 'Data/movies.dat'):
    movies = pd.read_csv(path, sep='::', engine='python', names=['movieID', 'title', 'genres'], encoding = 'latin1')

    return movies

# Preprocessing
def preprocess(movies):
    movies['tags'] = movies['genres'].str.replace('|', ' ', regex = False)

    cv = CountVectorizer(max_features = 5000, stop_words = 'english')
    vectors = cv.fit_transform(movies['tags']).toarray()

    similarity = cosine_similarity(vectors)

    return vectors, similarity

# Recommendation Engine
def recommend(title, movies, similarity_matrix, n = 5):
    try:
        index = movies[movies['title'].str.contains(title, case = False, regex = False)].index[0]
    except IndexError:
        return []
    
    distances = list(enumerate(similarity_matrix[index]))
    sorted_movies = sorted(distances, key = lambda x : x[1], reverse = True)[1 : n+1]

    return movies.iloc[[i[0] for i in sorted_movies]]['title'].tolist()

# Main Function
if __name__  == "__main__":
    movies = load_movies()

    i, similarity = preprocess(movies)

    while True:
        input_movie = input("Enter a movie title (or 'exit'): ")

        if input_movie.lower() == 'exit':
            break

        results = recommend(input_movie, movies, similarity)
        if results:
            print("\nRecommended Movies:")
            for movie in results:
                print(" -", movie)

        else:
            print("Movie not found.")
