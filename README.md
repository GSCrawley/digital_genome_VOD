# digital_genome_VOD

## Functional Requirements
### Customer registers to a service and selects a video and watches it

## Non-Functional Requirements
### The video Sever is deployed in multiple servers to provide auto-failover, scaling, and live-migration

## Best-Practice Policies
### The response time must be less than 30 second
### When video-servers are switched, user does not notice interruption

# Event Flow

### Video Service Genome (VSG) reads the service metamodel (nodes, node container images, and their connections)

### Spins up Autopoietic Manager (APM) and Cognitive Network Manager (CNM) and gives the details to CNM (Node urls and connections between nodes.)

### CNM sets up the connections and publishes the service url for users to access the service (service Durl to the client NS function).

### User connects to service url.
### CNM resolves the service url to the client and sets up the connection between the user and the client. Client is already connected to the server and the service is delivered from server to the user through the client.