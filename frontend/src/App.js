// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;


// src/App.js
import React, { useState } from 'react';

function App() {
  const [movie, setMovie] = useState('');
  const [movieData, setMovieData] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFetch = async () => {
    if (!movie) return;

    setLoading(true);
    try {
      // Step 1: Get recommendations from FastAPI backend
      const res = await fetch(`https://filmsy.vercel.app/recommend?movie=${movie}`);
      const data = await res.json();

      if (!data.recommendations || data.recommendations.length === 0) {
        alert('Movie not found or no recommendations.');
        setMovieData([]);
        setLoading(false);
        return;
      }

      // Step 2: Fetch movie posters/details from OMDb
      const OMDB_API_KEY = "13a42c81"; // Replace this with your OMDb key

      const detailedData = await Promise.all(
        data.recommendations.map(async (title) => {
          const response = await fetch(
            `https://www.omdbapi.com/?t=${encodeURIComponent(title)}&apikey=${OMDB_API_KEY}`
          );
          const info = await response.json();

          return {
            title: info.Title || title,
            poster: info.Poster !== "N/A" ? info.Poster : null,
            year: info.Year || '',
          };
        })
      );

      setMovieData(detailedData);
    } catch (err) {
      alert('Error fetching recommendations or posters.');
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10 px-4">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">🎬 Filmsy</h1>

      <div className="flex flex-col sm:flex-row gap-4 mb-8 w-full max-w-lg">
        <input
          type="text"
          value={movie}
          onChange={(e) => setMovie(e.target.value)}
          placeholder="Enter a movie name..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleFetch}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400"
        >
          {loading ? 'Loading...' : 'Get Recommendations'}
        </button>
      </div>

      {movieData.length > 0 && (
        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 max-w-6xl w-full">
          {movieData.map((movie, idx) => (
            <div
              key={idx}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition p-4 text-center"
            >
              {movie.poster ? (
                <img
                  src={movie.poster}
                  alt={movie.title}
                  className="w-full h-72 object-cover rounded mb-4"
                />
              ) : (
                <div className="w-full h-72 bg-gray-200 flex items-center justify-center text-gray-500 rounded mb-4">
                  No Image
                </div>
              )}
              <h2 className="text-lg font-semibold">{movie.title}</h2>
              <p className="text-sm text-gray-600">{movie.year}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;

