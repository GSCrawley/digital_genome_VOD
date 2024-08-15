
import pyTigerGraph as tg
import uuid
from datetime import datetime

# HIDE THESE
host = "https://55022d66f9ca4cf9b8b2a201dbe41306.i.tgcloud.io"
graphname = "VOD_associative_memory"
username = "user_4"
password = "Af6Jp2Qk3My4Is3/"
secret = "522gn5cetgv548s7qhhcspbr8ni5nuhn"

conn = tg.TigerGraphConnection(host=host, graphname=graphname, username=username, password=password)
conn.apiToken = conn.getToken(secret)

t = 1
# Event for user picking a video
def video_selected_event(data):
    global t
    event_id = f"T={str(t)}"
    video_id = data["selected_video"]
    # user_id = "U12345678"
    user_id = data["current_user"]
    # upsert Video vertex
    attributes = {
        "title": data["selected_video"]
    }
    conn.upsertVertex("Video", video_id, attributes)
    # upsert User vertex
    # attributes = {
    #     "name": "John"
    # }
    # conn.upsertVertex("User", user_id, attributes)
    # upsert Event vertex
    attributes = {
        "event_type": "video selection event",
        "sender": user_id,
        "receiver": video_id,
        "time": str(datetime.now().time())
    }
    conn.upsertVertex("Events", event_id, attributes)

    conn.upsertEdge("User", user_id, "user_event", "Events", event_id)
    conn.upsertEdge("Video", video_id, "video_event", "Events", event_id)
    conn.upsertEdge("User", user_id, "watches", "Video", video_id)

    t += 1
    return


def user_registration_event(data):
    user_id = f"U{str(uuid.uuid4())[:8]}"
    attributes = {
        "username": data['username'],
        "password": data['password'],
        "email": data['email']
    }
    conn.upsertVertex("User", user_id, attributes)
    print(data)

def validate_login(email, password):
    # email = data['email'],
    # password = data['password']
    result = conn.runInstalledQuery("authenticateUser", {"email": email, "password": password})
    if result[0] == {'Auth': []}:
        return('Fail')
    else:
        return(result[0])
 