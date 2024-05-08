import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import AWS from 'aws-sdk';
import axios from 'axios';
import dotenv from 'dotenv'
dotenv.config();

AWS.config.update({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION
});

const s3 = new AWS.S3();

interface Movie {
  id: string;
  name: string;
  url: string;
  subtitles?: string;
}

function Home() {
  const [moviesData, setMoviesData] = useState<{ movies: Movie[] } | null>(null);

  useEffect(() => {
    axios.get('http://localhost:5000/videos')
      .then(response => {
        setMoviesData({ movies: response.data.map((url, index) => ({ id: index.toString(), name: `Video ${index + 1}`, url })) });
      })
      .catch(error => {
        console.error('Error fetching videos', error);
      });
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