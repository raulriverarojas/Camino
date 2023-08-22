import PySimpleGUI as sg
from dotenv import load_dotenv
from dotenv import set_key
import os

# Define the window's contents
layout = [[sg.Text("Spotify API ClientID: ")],
          [sg.Input(default_text=os.getenv('SPOTIFY_CLIENT_ID'),key='spotify_client_id')],
          [sg.Text("Spotify API Client Secret: ")],
          [sg.Input(default_text=os.getenv('SPOTIFY_CLIENT_SECRET'),key='spotify_client_secret')],
          [sg.Text('Spotify folder'), sg.In(default_text=os.getenv('SPOTIFY_FOLDER'),size=(25,1), enable_events=True ,key='spotify_folder'), sg.FolderBrowse(initial_folder=os.getenv('SPOTIFY_FOLDER'))],
          [sg.Text("Soundcloud auth string: ")],
          [sg.Input(default_text=os.getenv('SOUNDCLOUD_AUTH_STR'),key='soundcloud_auth_string')],
          [sg.Text("Soundcloud client id: ")],
          [sg.Input(default_text=os.getenv('SOUNDCLOUD_CLIENT_ID'),key='soundcloud_client_id')],
          [sg.Text('Soundcloud folder'), sg.In(default_text=os.getenv('SOUNDCLOUD_FOLDER'),size=(25,1), enable_events=True ,key='soundcloud_folder'), sg.FolderBrowse(initial_folder=os.getenv('SOUNDCLOUD_FOLDER'))],
          [sg.Text(size=(40,1), key='output')],
          [sg.Button('Ok'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Window Title', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    window['output'].update('Running')

env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'.env')
if not os.path.exists(env_file_path):
    os.mknod(env_file_path)
set_key(dotenv_path=env_file_path,key_to_set='SOUNDCLOUD_FOLDER',value_to_set=window['soundcloud_folder'].get())
set_key(dotenv_path=env_file_path,key_to_set='SOUNDCLOUD_AUTH_STR',value_to_set=window['soundcloud_auth_string'].get())
set_key(dotenv_path=env_file_path,key_to_set='SOUNDCLOUD_CLIENT_ID',value_to_set=window['soundcloud_client_id'].get())
set_key(dotenv_path=env_file_path,key_to_set='SPOTIFY_FOLDER',value_to_set=window['spotify_folder'].get())
set_key(dotenv_path=env_file_path,key_to_set='SPOTIFY_CLIENT_ID',value_to_set=window['spotify_client_id'].get())
set_key(dotenv_path=env_file_path,key_to_set='SPOTIFY_CLIENT_SECRET',value_to_set=window['spotify_client_secret'].get())
# Finish up by removing from the screen
window.close()
