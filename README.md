# 🎬 Filmsy – Movie Recommendation Engine

**Filmsy** is a full-stack web application that recommends movies based on a given input movie using content-based filtering. It combines machine learning, modern web development, and third-party APIs to deliver a visually engaging and intelligent recommendation experience.

---

## Live Demo

- **Frontend (Vercel)**: [https://filmsy.vercel.app](https://filmsy.vercel.app)
- **Backend (Render)**: [https://filmsy-backend.onrender.com](https://filmsy-backend.onrender.com)

---

## 🛠 Tech Stack

### Backend (Machine Learning + API)
- **Python**
- **FastAPI**
- **pandas**, **scikit-learn** (for data processing & cosine similarity)
- **MovieLens 1M dataset** (for training the recommender)
- **Render** (for deployment)

### Frontend
- **ReactJS**
- **TailwindCSS**
- **Vercel** (for deployment)

### External APIs
- **OMDb API** – to fetch movie posters and metadata

---

## Machine Learning Methodology

1. **Data Source**:  
   [MovieLens 1M Dataset](https://grouplens.org/datasets/movielens/1m/)

2. **Preprocessing Steps**:
   - Read `movies.dat` file using custom delimiter `::`
   - Extract features from genres and titles
   - Construct a combined content feature for each movie

3. **Model**:
   - Used **TF-IDF Vectorizer** to convert text into numerical vectors
   - Calculated **cosine similarity** between movie vectors
   - Built an index for fast retrieval of top N most similar movies

4. **Serving**:
   - Exposed the recommender via a `/recommend` endpoint in FastAPI
   - The backend takes an input title and returns top similar titles

---

## Running the Project Locally

### 1. ⚙Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
