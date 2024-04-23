import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import LKUIVideoPlayer from "../components/LKUIVideoPlayer";
import JSONTestData from "../tests/movies.json";

function Player() {
  const { id } = useParams<{ id: string }>();
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

  // Find the movie object with the matching id
  const selectedMovie = movies.find((movie) => movie.id === id);

  if (!selectedMovie) {
    console.error("Movie not found for id:", id);
    return null;
  }

  // Extract title, URL, and subtitles from the selected movie
  const { name, url, subtitles } = selectedMovie;
  if (window.location.href.includes('lookeeloo-canary')) {
    document.title = `${name} - Lookeeloo (Canary [BETA])`
  } else if (window.location.href.includes('localhost')) {
    document.title = `${name} - Lookeeloo (running at localhost)`
  } else {
    document.title = `${name} - Lookeeloo`;
  }

  return (
    <div className="lkui-player-page">
      <LKUIVideoPlayer videoPath={url} captionsPath={subtitles} videoName={name} height={550}></LKUIVideoPlayer>
      <h2>{name}</h2>
    </div>
  );
}

export default Player;

interface Movie {
  id: string;
  name: string;
  url: string;
  subtitles?: string;
}
