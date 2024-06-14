import pyTigerGraph as tg
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

# HIDE THESE
host = os.getenv('TG_HOST')
graphname = os.getenv('TG_GRAPHNAME')
username = os.getenv('TG_USERNAME')
password = os.getenv('TG_PASSWORD')
secret = os.getenv('TG_SECRET')

conn = tg.TigerGraphConnection(host=host, graphname=graphname, username=username, password=password)
conn.apiToken = conn.getToken(secret)

# Event for user picking a video
def video_selected_event(data):
    event_id = f"E{str(uuid.uuid4())[:8]}"
    # video_id = f"V{str(uuid.uuid4())[:8]}"
    video_id = data
    user_id = "U12345678"
    # upsert Video vertex
    attributes = {
        "title": data
    }
    conn.upsertVertex("Video", video_id, attributes)
    # upsert User vertex
    attributes = {
        "name": "John"
    }
    conn.upsertVertex("User", user_id, attributes)
    # upsert Event vertex
    attributes = {
        "event_type": "video selection event",
        "sender": user_id,
        "receiver": video_id
    }
    conn.upsertVertex("Events", event_id, attributes)

    conn.upsertEdge("User", user_id, "user_event", "Events", event_id)
    conn.upsertEdge("Video", video_id, "video_event", "Events", event_id)
    conn.upsertEdge("User", user_id, "watches", "Video", video_id)

    return