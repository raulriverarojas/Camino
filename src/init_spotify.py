from functions import *
from scraping_functions import *
from dotenv import load_dotenv
import os
import re
load_dotenv()


create_command="mkdir -p "+os.getenv('SPOTIFY_FOLDER')
try: 
    os.system(create_command)
except Exception as e:
    print(e)

folders=topfoldersindir(os.getenv('SPOTIFY_FOLDER'))
sp=init_spotipy()
playlists=get_playlists_spotify(sp)
playlists=get_library_tracklist_spotify(sp, playlists)
for key, values in playlists.items():
    if values['name'] not in folders:

        create_command='mkdir -p '+os.path.join(os.getenv('SPOTIFY_FOLDER'),values['name'])
        try: 
            os.system(create_command)
        except Exception as e:
            print(e)
        save_hash('', '', os.path.join(os.getenv('SPOTIFY_FOLDER'),values['name']))
        save_like_list(values['tracks'],os.path.join(os.getenv('SPOTIFY_FOLDER'),values['name']), values['name'])



