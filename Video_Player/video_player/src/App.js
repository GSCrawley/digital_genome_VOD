import React from 'react';
import VideoPlayer from './VideoPlayer';
import './App.css';

// const videoJsOptions = {
//     autoplay: true,
//     controls: true,
//     responsive: true,
//     fluid: true,
//     sources: [{
//         src: '/Users/gideoncrawley/Projects/digital_genome_VOD/Video_Client/jack_straw.mp4',
//         type: 'video/mp4'
//     }]
// };

function App() {
  return (
      <div className="App">
          <h1>Video Streaming</h1>
          <VideoPlayer />
      </div>
  );
}

export default App;