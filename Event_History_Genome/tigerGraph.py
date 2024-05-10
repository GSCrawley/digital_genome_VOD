import config
import pyTigerGraph as tg
from spellchecker import SpellChecker
import uuid, json
import pandas as pd

# TigerGraph connection setup
conn = tg.TigerGraphConnection(
    host=config.tg_host, 
    graphname=config.tg_graph_name, 
    username=config.tg_username, 
    password=config.tg_password
)
conn.apiToken = conn.getToken(config.tg_secret)

def create_vertex(vertex_type, attributes):
    """Create a new vertex in the graph with the given attributes."""
    unique_id = uuid.uuid4()
    vertex_id = f"{vertex_type[0].upper()}{str(unique_id)[:8]}"
    conn.upsertVertex(vertex_type, vertex_id, attributes)
    print(f"Created vertex {vertex_type} with ID {vertex_id}")
    return vertex_id

def create_edge(from_vertex_type, from_vertex_id, edge_type, to_vertex_type, to_vertex_id, attributes=None):
    """Create a new edge in the graph between two vertices."""
    if attributes is None:
        attributes = {}
    conn.upsertEdge(from_vertex_type, from_vertex_id, edge_type, to_vertex_type, to_vertex_id, attributes)
    print(f"Created edge from {from_vertex_id} ({from_vertex_type}) to {to_vertex_id} ({to_vertex_type}) of type {edge_type}")

# Create Video Player vertices
player_id = create_vertex("Video_Player", {
    "player_id": "VPlayer1",
    "current_video_id": "None",
    "playback_state": "Stopped"
})

# Create Video Server vertices
server_id = create_vertex("Video_Server", {
    "server_id": "VServer1",
    "status": "Active",
    "URL": "http://server1.example.com/stream"
})

# Create User vertices
user_id = create_vertex("User", {
    "user_id": "User1",
    "user_name": "user1",
    "email": "user1@example.com"
})

# Create Video Content vertices
content_id = create_vertex("Content", {
    "content_id": "Content1",
    "title": "Example Movie",
    "genre": "Action"
})

# Create Video Library vertices
library_id = create_vertex("Video_Library", {
    "library_id": "Lib1",
    "owner_id": user1_id
})

# Create Events vertices
event_id = create_vertex("Events", {
    "event_id": "Event1",
    "type": "Play",
    "Timestamp": "2021-01-01T00:00:00Z"
})
# # Create Autopoietic Manager (APM) vertices
# apm_id = create_vertex("Autopoietic_Manager", {
#     "manager_id": "APM1",
#     "status": "Monitoring"
# })

# Create edges between vertices
create_edge("User", user_id, "Watches", "Video_Content", content_id)
create_edge("Video_Server", server_id, "Streams", "Video_Player", player_id)
create_edge("User", user_id, "HasLibrary", "Video_Library", library_id)
create_edge("Autopoietic_Manager", apm_id, "Manages", "Video_Server", server_id)
create_edge("Events", event_id, "Triggers", "Autopoietic_Manager", apm_id)

print("Completed creating vertices and edges.")
