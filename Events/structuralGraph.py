
import pyTigerGraph as tg
import uuid
from datetime import datetime

# HIDE THESE
host = "https://55022d66f9ca4cf9b8b2a201dbe41306.i.tgcloud.io"
graphname = "VOD_event_transaction_history"
username = "user_4"
password = "Af6Jp2Qk3My4Is3/"
secret = "1c016pgajvpj0ap0nviinddelrouf6ul"

conn = tg.TigerGraphConnection(host=host, graphname=graphname, username=username, password=password)
conn.apiToken = conn.getToken(secret)

# Event for user picking a video
def structural_setup_event(data):
    global CNM_id, SWM_id, UI_id, VS_id, Events_id
    # T = 0
    CNM_id = data['CNM']
    CNM_id = CNM_id.replace('http://', '')
    attributes = {}
    conn.upsertVertex("CNM", CNM_id, attributes)

    SWM_id = data['SWM']
    SWM_id = SWM_id.replace('http://', '')
    attributes = {}
    conn.upsertVertex("SWM", SWM_id, attributes)

    UI_id = data['UI']
    UI_id = UI_id.replace('http://', '')
    attributes = {}
    conn.upsertVertex("UI", UI_id, attributes)

    VS_id = data['video_server']
    VS_id = VS_id.replace('http://', '')
    attributes = {}
    conn.upsertVertex("Video_Server", VS_id, attributes)

    Events_id = data['Events']
    Events_id = Events_id.replace('http://', '')
    attributes = {}
    conn.upsertVertex("Events", Events_id, attributes)

    conn.upsertEdge("CNM", CNM_id, "CNM_SWM", "SWM", SWM_id)
    conn.upsertEdge("CNM", CNM_id, "CNM_UI", "UI", UI_id)
    conn.upsertEdge("CNM", CNM_id, "CNM_event", "Events", Events_id)

    conn.upsertEdge("SWM", SWM_id, "SWM_video_server", "Video_Server", VS_id)

    conn.upsertEdge("UI", UI_id, "UI_SWM", "SWM", SWM_id)
    conn.upsertEdge("UI", UI_id, "UI_event", "Events", Events_id)

    conn.upsertEdge("Video_Server", VS_id, "video_server_event","Events", Events_id)

    conn.upsertEdge("SWM", SWM_id, "SWM_event", "Events", Events_id)
    return

def client_connection_event(data):
    VC_id = data['video_client']
    VC_id = VC_id.replace('http://', '')
    UI_id = data['ui']
    UI_id = UI_id.replace('http://', '')
    edges = conn.getEdges("UI", UI_id)
    for edge in edges:
        if edge['e_type'] == 'UI_video_client':
            print("TEST:", edge)
            try:
                conn.delVerticesById(edge['to_type'], edge['to_id'])
                break
            except:
                pass
    attributes = {}
    # conn.upsertVertex("Events", )
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    conn.upsertVertex("Video_Client", VC_id, attributes)
    conn.upsertEdge("UI", UI_id, "UI_video_client", "Video_Client", VC_id)

    e_id = str(formatted_time)
    conn.upsertVertex("Events", e_id, attributes)
    conn.upsertEdge("UI", UI_id, "UI_event", "Events", e_id)
    conn.upsertEdge("Events", e_id, "video_client_event", "Video_Client", VC_id)

def create_video_client_event(data):
    VC_id = data['base']
    VC_id = VC_id.replace('http://', '')
    VC_id = VC_id[:-1]
    attributes = {}
    conn.upsertVertex("Video_Client", VC_id, attributes)
    conn.upsertEdge("CNM", CNM_id, "CNM_video_client", "Video_Client", VC_id)
    conn.upsertEdge("Video_Client", VC_id, "video_client_video_server", "Video_Server", VS_id)
    conn.upsertEdge("SWM", SWM_id, "SWM_video_client", "Video_Client", VC_id)
    conn.upsertEdge("Events", Events_id, "video_client_event", "Video_Client", VC_id)
    if VC_id == data['video_client'][0].replace('http://', ''):
        conn.upsertEdge("UI", UI_id, "UI_video_client", "Video_Client", VC_id)

