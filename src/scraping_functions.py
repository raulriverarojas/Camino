import yt_dlp
import re
import requests
import json
import os
import spotipy
from functions import *
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

def init_spotipy():

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                                               client_secret=os.getenv('CLIENT_SECRET'),
                                               redirect_uri=os.getenv('REDIRECT_URI'),
                                               scope="user-library-read"))

    response = sp.current_user_saved_tracks()['items']
    return sp

def get_likes_spotify(sp):
    try:
        response = sp.current_user_saved_tracks()['items']
        liked_tracks=[]
        for track in response:
            liked_tracks.append(track['track']['external_urls']['spotify'])
        return liked_tracks
    except Exception as e:
        print(e)

def get_playlists_spotify(sp):
    playlists={}
    next=True
    limit=50
    offset=0
    try:
        while(next):
            response = sp.current_user_playlists(limit,offset)
            for playlist in response['items']:
                name="".join([c for c in playlist['name'].replace(" ", "_") if re.match(r'\w', c)])
                playlists[str(playlist['external_urls']['spotify'])]={'name':name,'tracks':[]}
            offset+=limit
            if not response['next']:
                next=False
        return playlists
    except Exception as e:
        print(e)

def get_playlist_tracklist_spotify(sp, playlist):
    track_list=[]
    limited=False
    next=True
    limit=50
    offset=0
    try:
        while(next):
            response = sp.playlist_tracks(playlist, None, limit,offset)
            for track in response['items']:
                if 'CA' in track['track']['available_markets']:
                    track_list.append(track['track']['external_urls']['spotify'])
            offset+=limit
            if response['next'] is None:
                next=False
        return track_list
    except Exception as e:
        print(e)
def get_library_tracklist_spotify(sp, playlists):
    for playlist in playlists.keys():
        playlists[playlist]['tracks']=get_playlist_tracklist_spotify(sp, playlist)
    return playlists
def get_playlists_differences_spotify(playlists,dir_path):
    differences={}
    folders=topfoldersindir(dir_path)
    for key, values in playlists.items():
        if values['name'] in folders:
            track_list=read_like_list(os.path.join(dir_path,values['name']),values['name']+'.json')
            differences[os.path.join(dir_path, values['name'])]=find_likes_diff(track_list, values['tracks'])
    return differences
    
def download_differences_spotify(differences):
    for key, values in differences.items():
        if values:
            try:
                download_songs_spotify(values, key)
            except Exception as e:
                print(e)

def download_differences_soundcloud(differences):
    for key, values in differences.items():
        if values:
            try:
                download_songs_soundcloud(values, key)
            except Exception as e:
                print(e)

def save_differences(playlists, dir_path):
    folders=topfoldersindir(dir_path)
    for key, values in playlists.items():
        if values['name'] in folders:
            try:
                track_list=save_like_list(values['tracks'],os.path.join(dir_path,values['name']),values['name'])
            except Exception as e:
                print(e)





def create_new_playlists(playlists, dir_path):
    folders=topfoldersindir(dir_path)

    for key, values in playlists.items():
        if values['name'] not in folders:
            create_command='mkdir -p '+os.getenv('SOUNDCLOUD_FOLDER')+values['name']
            try: 
                os.system(create_command)
            except Exception as e:
                print(e)
            save_hash('', '', os.getenv('SOUNDCLOUD_FOLDER')+values['name'])
            save_like_list('', os.getenv('SOUNDCLOUD_FOLDER')+values['name'], values['name'])
            

    


def save_like_list(songs_list, dir_path, filename):
    write_out={
        'likes':songs_list,
    }
    with open(os.path.join(dir_path, filename+'.json'), 'w', encoding='utf-8') as f:
        json.dump(write_out, f, ensure_ascii=False, indent=4)
def read_like_list(dir_path, filename):
    try:
        full_path=os.path.join(dir_path,filename)
        f = open(full_path)
  
    # returns JSON object as 
    # a dictionary
        data = json.load(f)
  
        # Closing file                                                                                          
        f.close()
        return data['likes']
    except Exception as e:
        print(e)
        return '',''
def find_likes_diff(songs_list1, songs_list2):
    diff=[]
    for song1 in songs_list2:
        if song1 not in songs_list1:
            diff.append(song1)
    return diff


def init_soundcloud(auth_str, client_id, url):
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en;q=0.7',
    'Authorization': auth_str,
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://soundcloud.com',
    'Referer': 'https://soundcloud.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

    params = {
    'client_id': client_id,
    'limit': '100',
    'offset': '0',
    'linked_partitioning': '1',
    'app_version': '1681464840',
    'app_locale': 'en',
}
    try:
        response = requests.get(url, params=params, headers=headers)

    except Exception as e:
        print(e)
        return False
    return True
def get_likes_soundcloud(auth_str, client_id, url):
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en;q=0.7',
    'Authorization': auth_str,
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://soundcloud.com',
    'Referer': 'https://soundcloud.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

    params = {
    'client_id': client_id,
    'limit': '100',
    'offset': '0',
    'linked_partitioning': '1',
    'app_version': '1681464840',
    'app_locale': 'en',
}

    response = requests.get(url, params=params, headers=headers)

    data = response.text
    obj=json.loads(data)
    tracks=[]

    collections=obj['collection']
    for entry in collections:
        tracks.append(entry['track']['permalink_url'])
    return tracks
def  get_playlists_soundcloud(auth_str, client_id, url):
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en;q=0.7',
    'Authorization': auth_str,
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://soundcloud.com',
    'Referer': 'https://soundcloud.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

    params = {
    'client_id': client_id,
    'limit': '100',
    'offset': '0',
    'linked_partitioning': '1',
    'app_version': '1681464840',
    'app_locale': 'en',
}

    response = requests.get(url, params=params, headers=headers)

    data = response.text
    obj=json.loads(data)
    playlists={}

    collections=obj['collection']
    for entry in collections:
        playlists[str(entry['permalink_url'])]={'name':entry['permalink'], 'tracks':[]}
        for track in entry['tracks']:
            playlists[str(entry['permalink_url'])]['tracks'].append(str(track['id']))
    return playlists

def get_playlist_from_ids_soundcloud(auth_str, client_id, url, track_ids):
    tracks=[]
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en;q=0.7',
    'Authorization': auth_str,
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://soundcloud.com',
    'Referer': 'https://soundcloud.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}
    params=[]
    for track in track_ids:
        params.append({
    'ids': track,
    'client_id': client_id,
    'app_version': '1681464840',
    'app_locale': 'en',
})
    
    for param in params:
        response = requests.get(url, params=param, headers=headers)

        data = response.text
        obj=json.loads(data)
        tracks.append(obj[0]['permalink_url'])

    return tracks

def convert_playlists_id_to_tracklinks(playlists, auth_str, client_id, url):
    for key, value in playlists.items():
        playlists[key]['tracks']=get_playlist_from_ids_soundcloud(auth_str, client_id, url,playlists[key]['tracks'])
    return playlists
def download_songs_soundcloud(songs, dir_path):

    ydl_opts = {
    'format': 'mp3/128K/128K',
    'outtmpl': os.path.join(dir_path,'%(title)s.%(ext)s'),
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'restrictfilenames':True,
    'forcefilename':True,
}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        """ error_code = ydl.download(tracks) """
        for track in songs:
            info = ydl.extract_info(track, download=True)
            # Copy info dict and change video extension to audio extension
            info_with_audio_extension = dict(info)
            info_with_audio_extension['ext'] = 'mp3'
        # Return filename with the correct extension
            ydl.prepare_filename(info_with_audio_extension)
    
def download_songs_spotify(tracks, dir_path):
    try :
        command='spotdl '+' '.join(tracks)+' --config --output '+os.path.join(dir_path,"{title}.{output-ext}")
        os.system(command)
    except Exception as e:
        print(e)
