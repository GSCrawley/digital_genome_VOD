import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import logo from '../logo.svg';
import JSONTestData from "../tests/movies.json";

interface Movie {
  id: string;
  name: string;
  url: string;
  subtitles?: string;
}

function Home() {
  const [moviesData, setMoviesData] = useState<{ movies: Movie[] } | null>(null);

  useEffect(() => {
    // Set movies data directly from the imported JSON file
    setMoviesData(JSONTestData);
  }, []);
  if (!moviesData) {
    // Data not loaded yet
    return null;
  }

  const { movies } = moviesData;
  return (
    <div>
      <h1>Recommended for you</h1>
      {movies.map((movie: Movie) => (
        <Link to={`/player/${movie.id}`}>
          <div className='lkui-movie-select-devchannel' key={movie.id}>
            <h2>{movie.name}</h2>
          </div>
        </Link>
      ))}
    </div>
  );
}

export default Home;
