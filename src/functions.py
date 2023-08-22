import os
import json
import hashlib
from os import walk
import logging


def init_Savify(client_id, client_secret, download_path):

    """ s = Savify(api_credentials=(client_id, client_secret), path_holder=PathHolder(downloads_path=download_path), quality=Quality.Q128K, download_format=Format.MP3, group='%artist%/%album%', skip_cover_art=True) """
    s = Savify(api_credentials=(client_id, client_secret),path_holder=PathHolder())

    # Spotify URL
    return s
def download_track(s, url):
    s.download(url, query_type=Type.TRACK)
    

def sha1OfFile(filepath):
    sha=hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2**10) # Magic number: one-megabyte blocks.
            if not block:
                break
            sha.update(block)
    return sha.hexdigest()

def hash_files(dir_path, hashes):
    for (path, dirs, files) in os.walk(dir_path):
        for file in sorted(files): # we sort to guarantee that files will always go in the same order
            """ hashes.append(sha1OfFile(os.path.join(path, file))) """
            if('.mp3' in file):
                hashes.append(sha1OfFile(os.path.join(path, file)))

        for dir in sorted(dirs): # we sort to guarantee that dirs will always go in the same order
            """ hashes.append(hash_dir(os.path.join(path, dir))) """
            hash_files(os.path.join(path, dir), hashes)
    
    return hashes
def hash_hashes(hashes):
    hash_str=''.join(hashes)
    """ print('hash hashes hash_str: {}'.format(hash_str)) """
    sha3=hashlib.sha1()
    sha3.update(hash_str.encode())
    return sha3.hexdigest()

def hash_dir(dir_path):
    hashes=[]
    hashes=hash_files(dir, hashes)
    combined_hash=hash_hashes(hashes)
    return combined_hash, hashes

def filesindir(dir_path):

    onlyfiles = []
    for (dirpath, dirnames, filenames) in walk(dir_path):
        onlyfiles.extend(filenames)

    """ onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))] """
    return onlyfiles
def topfoldersindir(dir_path):

    folders = []
    for (dirpath, dirnames, filenames) in walk(dir_path):
        folders.extend(dirnames)
        break
    """ onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))] """
    return folders

def find_diff(hashes, dir_path, differences):

    for (path, dirs, files) in os.walk(dir_path):
        for file in sorted(files): # we sort to guarantee that files will always go in the same order
            """ hashes.append(sha1OfFile(os.path.join(path, file))) """
            if('.mp3' in file):
                hash_cal=sha1OfFile(os.path.join(path, file))
                if (os.path.join(path, file) not in differences and hash_cal not in hashes ):
                    differences.append(os.path.join(path, file))

        for dir in sorted(dirs): # we sort to guarantee that dirs will always go in the same order
            """ hashes.append(hash_dir(os.path.join(path, dir))) """
            find_diff(hashes, os.path.join(path, dir), differences)
    
    return differences
def save_hash(hashes, combined_hash, dir_path):

    write_out={
        'hashes':hashes,
        'master_hash':combined_hash
    }
    with open(os.path.join(dir_path, 'hash.json'), 'w', encoding='utf-8') as f:
        json.dump(write_out, f, ensure_ascii=False, indent=4)
        
def read_hash(dir_path, filename):
    try:
    
        f = open(os.path.join(dir_path,'hash.json'))
  
    # returns JSON object as 
    # a dictionary
        data = json.load(f)
  
        # Closing file                                                                                          
        f.close()
        return data['hashes'], data['master_hash']
    except:
        return '',''
    
def copy_differences(differences, new_dir_path):
    for filename in differences:
        new_file_name=os.path.join(new_dir_path, os.path.basename(filename))
        #print('new file name {}'.format(new_file_name))
        command='copy '+'\"{}\"'.format(filename)+' \"{}\"'.format(new_file_name)
        #print('copy differences: {}'.format(command))
        os.popen(command)
def hash_and_copy_folder(dir_path, copy_to):
    old_hashes, old_master_hash=read_hash(dir_path, 'hash.json')
    hashes=[]
    differences=[]
    hashes=hash_files(dir_path, hashes)
    combined_hash=hash_hashes(hashes)
    find_diff(old_hashes, dir_path, differences)
    copy_differences(differences, copy_to)
    save_hash(hashes, combined_hash, dir_path)
