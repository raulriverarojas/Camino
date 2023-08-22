from functions import *
from scraping_functions import *
from dotenv import load_dotenv
import os
import re
load_dotenv()


create_command="mkdir -p "+os.getenv('SOUNDCLOUD_FOLDER')
try: 
    os.system(create_command)
except Exception as e:
    print(e)

folders=topfoldersindir(os.getenv('SOUNDCLOUD_FOLDER'))

if init_soundcloud(os.getenv('AUTH_STR'), os.getenv('CLIENT_ID_SOUNDCLOUD'), os.getenv('ACCOUNT_URL')):
    playlists=get_playlists_soundcloud(os.getenv('AUTH_STR'), os.getenv('CLIENT_ID_SOUNDCLOUD'), os.getenv('PLAYLIST_URL'))
    playlists=convert_playlists_id_to_tracklinks(playlists, os.getenv('AUTH_STR'), os.getenv('CLIENT_ID_SOUNDCLOUD'), os.getenv('TRACK_ID_URL'))
    for key, values in playlists.items():
        if values['name'] not in folders:
            create_command='mkdir -p '+os.path.join(os.getenv('SOUNDCLOUD_FOLDER'),values['name'])
            try: 
                os.system(create_command)
            except Exception as e:
                print(e)
            save_hash('', '', os.path.join(os.getenv('SOUNDCLOUD_FOLDER'),values['name']))
            save_like_list(values['tracks'], os.path.join(os.getenv('SOUNDCLOUD_FOLDER'),values['name']), values['name'])
else: 
    print('Error initializing soundcloud')