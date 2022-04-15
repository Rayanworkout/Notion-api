import requests
import json


def prettify_db(topic, db):
    data = dict()
    entries = db["results"]
    for entry in entries:
        name = entry["properties"]["Name"]["title"][0]["plain_text"]
        author = entry["properties"]["Author"]["select"]["name"]
        themes = entry["properties"]["Themes"]["multi_select"][0]["name"]
        ressource_type = entry["properties"]["Type"]["select"]["name"]
        url =  entry["properties"]["URL"]['url']
        
        #####################################################
        
        data[name] = dict()
        data[name]["author"] = author
        data[name]["themes"] = themes
        data[name]["type"] = ressource_type
        data[name]["url"] = url
        
        # THESE THEMES DO NOT HAVE "ACCESSIBILITY" FIELD
        if topic not in ["psycho-socio", "sciences", "histoire-geopolitique",  "dev-perso", "alimentation", "livres-films-series"]:         
            accessibility = entry["properties"]["Accessibility"]["multi_select"][0]['name']
            data[name]["accessibility"] = accessibility
    return data
        
def pull_db():
    # SETTING UP HEADERS
    headers = {
    "Authorization": "Bearer NOTION_API_TOKEN",
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
    }
    # GETTING THEMES LIST FROM JSON DB
    with open("files/database.json", "r", encoding="utf8") as file:
        db = json.load(file)["databases_id"]

    topics = [topic for topic in db]
    database = dict()
    # LOOPING THROUGH ALL DB TO FILTER INFO AND GET DATA
    for topic in topics:
        url = f"https://api.notion.com/v1/databases/{db[topic]}/query"


        response = requests.post(url, headers=headers).json()
        database[topic] = prettify_db(topic, response)

        print(topic, "ok")
    # WRITE RELEVANT DATA TO A DB
    with open('files/my_file.json', 'w', encoding='utf8') as file:
        json.dump(database, file)
        print("File created.")
