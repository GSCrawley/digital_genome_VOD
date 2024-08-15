# digital_genome_VOD

## Servers must be run in the following order, in the following ports: 
### Video Server :5005
### Video Client :5001
### User Interface :5000
### Cognitive Network Manager :5004 - this will send user back to the user interface at 5000

## Functional Requirements
### Customer registers to a service and selects a video and watches it

## Non-Functional Requirements
### The video Sever is deployed in multiple servers to provide auto-failover, scaling, and live-migration

## Best-Practice Policies
### The response time must be less than 30 second
### When video-servers are switched, user does not notice interruption

# Event Flow

### User registers creating a new account

### User Logs In
### User is presented with list of videos in their account, which are stored in AWS S3 bucket. They can play a video, upload a new video, or delete a video.
### They can also adjust the video player size, volume, and playback speed.

### The global associative memory and event history will have memory of current video buffer status and when a server shuts down, new server will start the video from the last read. The way this will work is an event history will be established through event listeners in the player (play/pause, ffwd, rwnd, stop, as well as player and buffer heads). The player head in the player will record the current timestamp and send it to the buffer head in the video client, constantly updating the buffer status so that the video client can play the video from the last read. This event history will be stored in Event_History_Genome

### CNM resolves the service url to the client and sets up the connection between the user and the client. Client is already connected to the server and the service is delivered from server to the user through the client.
