import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import AWS from 'aws-sdk';


require('dotenv').config();


AWS.config.update({
  accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
//   secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
  region: process.env.REACT_APP_AWS_REGION
});

const s3 = new AWS.S3();

const getVideoList = async () => {
    const params = {
      Bucket: process.env.REACT_APP_S3_BUCKET_NAME,
    };
  
    try {
      const s3_Response = await s3.listObjectsV2(params).promise();
      const video_List = s3_Response.Contents.map((video) => {
        // Generate signed URL if private, else use the direct S3 link
        const url = video.Key; // Modify this line to gepnerate a signed URL if needed
        return url;
      });
      return video_List;
    } catch (err) {
      console.error("Error fetching videos from S3", err);
      return [];
    }
  };
  
  const uploadVideo = async (file) => {
    const params = {
      Bucket: process.env.REACT_APP_S3_BUCKET_NAME,
      Key: file.name, // The filename as the key for the object
      Body: file,
      ContentType: file.type
    };
  
    try {
      await s3.putObject(params).promise();
      console.log("Successfully uploaded video.");
      // Optionally, refresh the video list here
    } catch (err) {
      console.error("Error uploading video to S3", err);
    }
  };

  const deleteVideo = async (videoKey) => {
    const params = {
      Bucket: process.env.REACT_APP_S3_BUCKET_NAME,
      Key: videoKey,
    };
  
    try {
      await s3.deleteObject(params).promise();
      console.log("Successfully deleted video.");
      // Optionally, refresh the video list here
    } catch (err) {
      console.error("Error deleting video from S3", err);
    }
  };

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
    setMoviesData(getVideoList);
  }, []);
  if (!moviesData) {
    // Data not loaded yet
    return null;
  }

    // const { movies } = moviesData;
    //     return (
    //         <div>
    //         <h1>Recommended for you</h1>
    //         {movies.map((movie: Movie) => (
    //             <Link to={`/player/${movie.id}`}>
    //             <div className='lkui-movie-select-devchannel' key={movie.id}>
    //                 <h2>{movie.name}</h2>
    //             </div>
    //             </Link>
    //         ))}
    //         </div>
    //     );
    //     }
}

export default Home