import config
import pyTigerGraph as tg
from spellchecker import SpellChecker
import uuid, json
import pandas as pd

host = config.tg_host
graphname = config.tg_graph_name
user_name = config.tg_user_name
password = config.tg_password
secret = config.tg_secret

conn = tg.TigerGraphConnection(host=host, graphname=graphname, username=username, password=password)
conn.apiToken = conn.getToken(secret)

def create_new_user_vertex(first_name, last_name, user_name, password, email, join_date):
    unique_id = uuid.uuid4()
    user_id = f"P{str(unique_id)[:8]}"
    join_date = int(mm/dd/yyyy)
    attributes = {
        "first_name": first_name,
        "last_name": last_name,
        "user_name": user_name,
        "password": password,
        "email": email,
        "join_date": join_date
    }
    print(attributes)
    conn.upsertVertex("User", attributes)
    return(user_id)

def create_new_video_vertex(name, year_released, length, genre, director, source):
    unique_id = uuid.uuid4()
    video_id = unique_id
    year_released = int(year_released)
    attributes = {
        "name": name,
        "genre": genre,
        "director": director,
        "source": source,
    }
    print(attributes)
    conn.upsertVertex("Content", care_provider_id, attributes)
    return(video_id)

def user_login(email, password):
    result = conn.runInstalledQuery("authenticateUser", {"email": email, "password": password})
    # print('RESULT: ', result[0]['User'])
    return result[0]

def get_user_profile(id_value):
    result = conn.runInstalledQuery("getProfile", {"id_value": id_value})
    # print(result)
    return result

def user_add_video(user_id, video_id):
    properties = {"weight": 5}
    result = conn.upsertEdge("User", f"{user_id}", "uploading", "Video", f"{video_id}", f"{properties}")
    return result

def get_user_info(id_value):
    result = conn.runInstalledQuery("getPatientInfo", {"id_value": id_value})
    info = result[0]['User'][0]['attributes']['User.DOB']
    return info

def get_video_info(id_value_data):
    id_value_list = json.loads(id_value_data)
    result_list = []
    for id_value in id_value_list:
        print("ID_VALUE:", id_value)
        result = conn.runInstalledQuery("getSymptomInfo", {"id_value": id_value})
        name = result[0]['Symp'][0]['attributes']['Symp.name']
        result_list.append(name)
    return result_list

def check_existing_video(user_id, video_list_data):
    vertex_type = "Video"
    attribute = "name"
    result_list = []
    id_list = []
    spell = SpellChecker()
    # SPELL CHECKER
    for video in video_list_data:
        video_check = video.split(" ")
        checked_words = []
        for word in video_check:
            # print("WORD: ", word)
            checked_word = spell.correction(word)
            checked_words.append(checked_word)
        result = " ".join(checked_words)
        result_list.append(result.lower())
    result_list = video_list_data
    print('RESULT: ', result_list)
    try:
        df = conn.getVertexDataFrame(vertex_type)
        for name in result_list:
            if name[-1] == ".":
                name = name[:-1]
            if name in df['name'].values:
                # print(df['name'].values)
                print("EXISTING VIDEO: ", name)
                result = df.loc[df[attribute] == name]
                v_id = result['v_id'].values
                v_id = str(v_id)[2:-2]
                # print(df.loc[df[attribute]==name])
                # edge.s.append(v_id)
                id_list.append(v_id)
                properties = {"weight": 5}
                print("test", v_id)
                conn.upsertEdge("User", f"{user_id}", "is_watching", "Video", f"{v_id}", f"{properties}")
            else:
                v_id = create_video_vertex(user_id, name)
                print("v_id: ", v_id)
                id_list.append(v_id)
    except Exception as e:
        print("test")
        for name in result_list:
            v_id = create_video_vertex(user_id, name)
            id_list.append(v_id)
    return(id_list)


