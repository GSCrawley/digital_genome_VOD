import React, { useEffect, useRef, useState } from 'react';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';

const VideoPlayer = () => {
    const videoRef = useRef(null);
    const playerRef = useRef(null);
    const [videoUrl, setVideoUrl] = useState('');

    useEffect(() => {
        fetch('/current_server_url')
            .then(response => response.json())
            .then(data => {
                setVideoUrl(data.url + '/video_feed');
            });

        // Make sure Video.js player is only initialized once
        if (videoUrl && !playerRef.current) {
            const videoElement = videoRef.current;
            if (!videoElement) return;

            playerRef.current = videojs(videoElement, {
                autoplay: true,
                controls: true,
                responsive: true,
                fluid: true,
                sources: [{
                    src: videoUrl,
                    type: 'video/mp4'
                }]
            }, () => {
                console.log('player is ready');
            });
        }

        return () => {
            if (playerRef.current) {
                playerRef.current.dispose();
                playerRef.current = null;
            }
        };
    }, [videoUrl]);

    return (
        <div data-vjs-player>
            <video ref={videoRef} className="video-js" />
        </div>
    );
};

export default VideoPlayer;
