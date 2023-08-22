from functions import *
from scraping_functions import *
from dotenv import load_dotenv
import os
import re
load_dotenv()

folders=topfoldersindir(os.getenv('SOUNDCLOUD_FOLDER'))

if init_soundcloud(os.getenv('AUTH_STR'), os.getenv('CLIENT_ID_SOUNDCLOUD'), os.getenv('ACCOUNT_URL')):
    playlists=get_playlists_soundcloud(os.getenv('AUTH_STR'), os.getenv('CLIENT_ID_SOUNDCLOUD'), os.getenv('PLAYLIST_URL'))
    create_new_playlists(playlists, os.getenv('SOUNDCLOUD_FOLDER'))
    playlists=convert_playlists_id_to_tracklinks(playlists, os.getenv('AUTH_STR'), os.getenv('CLIENT_ID_SOUNDCLOUD'), os.getenv('TRACK_ID_URL'))
    differences=get_playlists_differences_spotify(playlists, os.getenv('SOUNDCLOUD_FOLDER'))
    download_differences_soundcloud(differences)
    save_differences(playlists, os.getenv('SOUNDCLOUD_FOLDER'))

    """ for key, values in playlists.items():
        if values['name'] in folders:
            old_like_list=read_like_list(os.getenv('SOUNDCLOUD_FOLDER'), values['name']+'.json')
            try: 
                os.system(create_command)
            except Exception as e:
                print(e)
            save_hash('', '', os.getenv('SOUNDCLOUD_FOLDER')+values['name'])
            save_like_list(values['tracks'], os.getenv('SOUNDCLOUD_FOLDER')+values['name'], values['name']) """
else: 
    print('Error initializing soundcloud')
for folder in folders:
    hash_and_copy_folder(os.path.join(os.getenv('SOUNDCLOUD_FOLDER'), folder), os.getenv('DESTINATION_FOLDER'))
    
