from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from engine import load_movies, preprocess, recommend

# Load and prepare model on startup
movies = load_movies()
_, similarity = preprocess(movies)

# Create app
app = FastAPI()

# Enable CORS so React can access it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Movie Recommendation API is running"}

@app.get("/recommend")
def recommend_movies(movie: str = Query(..., description="Movie title to search")):
    results = recommend(movie, movies, similarity)
    if not results:
        return {"error": "Movie not found"}
    return {"recommendations": results}
