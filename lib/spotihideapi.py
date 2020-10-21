###############################################################################
## Steganographic tool developed as an end-of-master's thesis at the Carlos III 
## University of Madrid that hides information in public playlists of spotify.
###############################################################################
## Author: Jose Carlos Quiroga Alvarez
## Copyright: Copyright 2020, SpotiHide2
## Email: kh4r0nt3@protonmail.com
## Status: Development
###############################################################################

import math
import time
import spotipy
import secrets
import colored
import progressbar
from os import path
from terminaltables import AsciiTable

class SpotiHideApi(object):

    def __init__(self):
        self.__username = ''
        self.__scope = 'playlist-read-private playlist-modify-private playlist-modify-public'
        self.__client_id = ''
        self.__client_secret = ''

        self.__redirect_uri = 'http://localhost:8080/callback'
        self.__spotify = None

        self.__artist_list = []
        self.__track_list = []

        self.__artist_table = [["Artist"]]
        self.__track_table = [["Track"]]
        self.__encode_table = [["Track", "Artist", "Integer", "Binary"]]
    

    
    def spotify_console(self):
        """
        """
        switch = {'encode':self.encode, 'decode':self.decode, 'show':self.show, 'update':self.update, 'help':self.help, 'exit': self.exit}
        self.auth()
        print(colored.stylize("""\n[*] """, colored.fg("light_green_3")) + "Generating binary alphabet with 256 artists\n")
        self.search_artists(50, 256)
        while True:
            command = input(colored.stylize("""\nSpotify > """, colored.fg("light_green_3")))
            params = command.split()
            try:
                switch[params[0]](*params[1:])
            except KeyError:
                print(colored.stylize("""\n[*] """, colored.fg("light_red")) + 'Unknown command: %s\n' % (command))
            except IndexError:
                try:
                    switch[params[0]]()
                except KeyError:
                    print(colored.stylize("""\n[*] """, colored.fg("light_red")) + 'Unknown command: %s\n' % (command))
                except IndexError:
                    pass
            except SystemExit:
                return

    def show(self,
            *args):
        """
        """
        if args and len(args) == 1 and args[0] == 'artists':
            print(AsciiTable(self.artist_table).table)
        elif args and len(args) == 1 and args[0] == 'tracks':
            for track in self.track_list:
                tracks = ''
                for tr in track[:2]:
                    tracks = str(tr[0][:20]) + ', ' + tracks 
                self.track_table = [tracks]   
            print(AsciiTable(self.track_table).table)
        elif args and len(args) == 1 and args[0] == 'all':
            all_table = [["Artist", "Tracks"]]
            lista = []
            for track in self.track_list:
                tracks = ''
                for tr in track[:2]:
                    tracks = str(tr[0][:30]) + ', ' + tracks
                lista.append(tracks)   
            for artist, track in zip(self.artist_list, lista):
                all_table.append([artist, track])
            print(AsciiTable(all_table).table)
        else:
            print("\nUsage:\tshow artists\n\tshow tracks\n\tshow all")
            raise KeyError
    
    def update(self,
            *args):
        """
        """
        if args and len(args) == 3 and args[0] == 'artists' and int(args[1]) <= 50 and int(args[2]) in [256,512,1024]:
            print(colored.stylize("""\n[*] """, colored.fg("light_green_3")) + f"Updating binary alphabet with {args[2]} artists\n")
            del self.artist_list[:]
            del self.artist_table[1:]
            self.search_artists(int(args[1]), int(args[2]))
        elif args and len(args) == 2 and args[0] == 'tracks' and int(args[1]) <= 50:
            del self.track_list[:]
            del self.track_table[1:]
            print(colored.stylize("""\n[*] """, colored.fg("light_green_3")) + f"Updating track list with {args[1]} tracks\n")
            [self.search_tracks(artist, int(args[1])) for artist in self.artist_list]
        else:
            print("\nUsage:\tupdate artists ENTROPY BITS\n\tupdate tracks ENTROPY")
            raise KeyError

    def encode(self,
            *args):
        """
        """
        if args and len(args) == 4 and args[0] == 'filename' \
                                   and path.exists(args[1]) \
                                   and path.isfile(args[1]):
            with open(args[1]) as f:
                data = f.read().splitlines()
            try:
                for line in data:
                    del self.encode_table[1:]
                    self.encode_msg(self.username, args[2], line) #Username, File, Line
                    print(AsciiTable(self.encode_table).table + '\n')
                    print(colored.stylize("""[*] """, colored.fg("light_green_3")) + f"Message: {line}\n")
                    time.sleep(int(args[3])) #Threshold
            except KeyboardInterrupt:
                return
        elif args and len(args) >= 2:
            try:
                del self.encode_table[1:]
                self.encode_msg(self.username, args[0], ' '.join(args[1:])) #Playlist Name, Message
                print(AsciiTable(self.encode_table).table + '\n')
                print(colored.stylize("""[*] """, colored.fg("light_green_3")) + f"Message: {' '.join(args[1:])}\n")
            except Exception:
                raise KeyError  
        else:
            print("\nUsage:\tencode filename PATH PLAYLIST THRESHOLD\n\tencode PLAYLIST MESSAGE")
            raise KeyError

    def decode(self,
            *args):
        """
        """
        if args and len(args) == 4 and args[0] == 'local':
            try:
                while True:
                    decode_local_table = self.decode_local_msg(args[1], args[2])
                    print(AsciiTable(decode_local_table).table + '\n')
                    time.sleep(int(args[3])) #Threshold
            except KeyboardInterrupt:
                return
        elif args and len(args) == 3 and args[0] == 'local':
            try:
                while True:
                    decode_local_table = self.decode_local_msg(self.username, args[1])
                    print(AsciiTable(decode_local_table).table + '\n')
                    time.sleep(int(args[2])) #Threshold
            except KeyboardInterrupt:
                return
        elif args and len(args) == 3:
            try:
                while True:
                    del self.encode_table[1:]
                    message = self.decode_msg(args[0], args[1]) #Username, Playlist Name
                    if len(self.encode_table) > 1:
                        print(AsciiTable(self.encode_table).table + '\n')
                    print(colored.stylize("""[*] """, colored.fg("light_green_3")) + f"Message: {message}\n")
                    time.sleep(int(args[2])) #Threshold
            except KeyboardInterrupt:
                return
        elif args and len(args) == 2:
            try:
                while True:
                    del self.encode_table[1:]
                    message = self.decode_msg(self.username, args[0]) #Playlist Name
                    if len(self.encode_table) > 1:
                        print(AsciiTable(self.encode_table).table + '\n')
                    print(colored.stylize("""[*] """, colored.fg("light_green_3")) + f"Message: {message}\n")
                    time.sleep(int(args[1])) #Threshold
            except KeyboardInterrupt:
                return
        else:
            print("\nUsage:\tdecode local [USERNAME] PLAYLIST THRESHOLD\n\tdecode [USERNAME] PLAYLIST THRESHOLD")
            raise KeyError

    def help(self, *args):
        if not args:
            print(colored.stylize("""\n[*] """, colored.fg("light_green_3")) + "Usage:\tshow artists\n\t\tshow tracks\n\t\tshow all")
            print("\n\t\tupdate artists ENTROPY BITS\n\t\tupdate tracks ENTROPY")
            print("\n\t\tencode filename PATH PLAYLIST THRESHOLD\n\t\tencode PLAYLIST MESSAGE")
            print("\n\t\tdecode local [USERNAME] PLAYLIST THRESHOLD\n\t\tdecode [USERNAME] PLAYLIST THRESHOLD")
        else:
            raise KeyError
    
    def exit(self, *args):
        """Exit function.
        """
        if not args:
            raise SystemExit
        else:
            raise KeyError

    def auth(self):
        """
        Authenticates the user through a token to obtain the spotify object.
        """
        token = spotipy.util.prompt_for_user_token(self.username,
                                                   self.scope,
                                                   client_id = self.client_id,
                                                   client_secret = self.client_secret,
                                                   redirect_uri= self.redirect_uri)
        if token:
            self.spotify = spotipy.Spotify(auth=token)
        else:
            print(colored.stylize("""\n[*] """, colored.fg("light_red")) + 'Cant get token for: %s\n' % (self.username))
            exit()
    
    def add_playlist_tracks(self, username, playlist_name, track_list):
        """
        Adds a list of tracks to the playlist.
        """
        playlist_id = self.get_playlist_id(username, playlist_name)
        request_chunks = [track_list[i:i + 100] for i in range(0, len(track_list), 100)] # Blocks of 100 songs
        for track_chunk in request_chunks:
            self.spotify.user_playlist_add_tracks(username, playlist_id, track_chunk)

    def delete_playlist_tracks(self, username, playlist_name):
        """
        Deletes all the tracks from a playlist.
        """
        playlist_id = self.get_playlist_id(username, playlist_name)
        track_list = self.get_playlist_tracks_id(username, playlist_name)
        request_chunks = [track_list[i:i + 100] for i in range(0, len(track_list), 100)] # Blocks of 100 songs
        for track_chunk in request_chunks:
            self.spotify.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, track_chunk)

    def get_playlist_id(self, username, playlist_name):
        """
        Returns the id of a playlist by searching on each result page for its name.
        """
        playlist_id = ''
        playlists = self.spotify.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                return playlist_id
        while playlists['next']: # If there are more playlists
            playlists = self.spotify.next(playlists)
            for playlist in playlists['items']:
                if playlist['name'] == playlist_name:
                    playlist_id = playlist['id']
                    return playlist_id
        return playlist_id

    def get_playlist_tracks_id(self, username, playlist_name):
        """
        Returns a list with all the identifiers of the tracks on a playlist.
        """
        track_list = []
        playlist_id = self.get_playlist_id(username, playlist_name)
        tracks = self.spotify.playlist_tracks(playlist_id)
        for i in range(len(tracks['items'])):
            track_list.append(tracks['items'][i]['track']['id'])
        while tracks['next']: # If there are more tracks
            tracks = self.spotify.next(tracks)
            for i in range(len(tracks['items'])):
                track_list.append(tracks['items'][i]['track']['id'])
        return track_list

    def get_playlist_artists(self, username, playlist_name):
        """
        Returns a list with the first artist of all the tracks on a playlist.
        """
        artists = []
        playlist_id = self.get_playlist_id(username, playlist_name)
        tracks = self.spotify.playlist_tracks(playlist_id)
        for i in range(len(tracks['items'])):
            artists.append((tracks['items'][i]['track']['name'], tracks['items'][i]['track']['artists'][0]['name'])) # Appends the first artist and track
        while tracks['next']: # If there are more tracks
            tracks = self.spotify.next(tracks)
            for i in range(len(tracks['items'])):
                artists.append((tracks['items'][i]['track']['name'], tracks['items'][i]['track']['artists'][0]['name']))
        return artists     

    def get_playlist_info(self, username, playlist_name):
        """
        Returns the local files library metadata
        """
        playlist_info = []
        playlist_id = self.get_playlist_id(username, playlist_name)
        playlist_items = self.spotify.playlist_tracks(playlist_id)
        for i in range(len(playlist_items['items'])):
            print(playlist_items['items'][i])
            playlist_info.append([playlist_items['items'][i]['track']['name'], 
                        playlist_items['items'][i]['track']['artists'][0]['name'],
                        playlist_items['items'][i]['track']['album']['name']])
        while playlist_items['next']: # If there are more tracks
            playlist_items = self.spotify.next(playlist_items)
            for i in range(len(playlist_items['items'])):
                playlist_info.append([playlist_items['items'][i]['track']['name'], 
                        playlist_items['items'][i]['track']['artists'][0]['name'],
                        playlist_items['items'][i]['track']['album']['name']])
        return playlist_info
                                                                                                                                                                            

    def search_artists(self, entropy, bits):
        """
        Generates the artist alphabet
        """
        replace_artist = []
        offset_list = list(range(0, bits-50, 50)) + [bits-50]
        new_offset = offset_list[len(offset_list)-1]
 
        for offset in offset_list:
            artists = self.spotify.search(q='a', type='artist', offset=offset, limit=50)
            for artist in progressbar.progressbar(artists['artists']['items']):
                if artist['name'] not in self.artist_list and self.search_tracks(artist['name'], entropy):
                    self.artist_list = artist['name']
                    self.artist_table = [artist['name']]
                elif artist['name'] not in self.artist_list and artist['name'] not in replace_artist:
                    replace_artist.append(artist['name'])
        size = len(self.artist_list) + len(replace_artist)

        if size < bits:
            for i in range(bits-size):
                replace_artist.append('Padding')
 
        while len(replace_artist) > 0:
            new_offset = new_offset + len(replace_artist)
            artists = self.spotify.search(q='a', type='artist', offset=new_offset, limit=50)
            for artist in artists['artists']['items']:
                if artist['name'] not in self.artist_list and self.search_tracks(artist['name'], entropy):
                    del replace_artist[0]
                    self.artist_list = artist['name']
                    self.artist_table = [artist['name']]
                elif artist['name'] not in self.artist_list and artist['name'] not in replace_artist: 
                    del replace_artist[0]
                    replace_artist.append(artist['name'])
    
    def search_tracks(self, artist, entropy):
        """
        Searches tracks
        """
        filtered_track_list = []
        tracks = self.spotify.search(q='artist:' + artist, type='track', limit=entropy) # Searchs among the first limit tracks
        if len(tracks['tracks']['items']) == 0:
            return False
        else:
            for track in tracks['tracks']['items']:
                if track['artists'][0]['name'] == artist: # Filters the track artist
                    filtered_track_list.append((track['name'], track['id']))
            if len(filtered_track_list) > 0:
                self.track_list.append(filtered_track_list)
                return True
            return False
        
    def encode_msg(self, username, playlist_name, message):
        """
        Encodes the message
        """
        track_list = []
        self.delete_playlist_tracks(username, playlist_name)
        binary = self.to_bin(message)
        bits = round(math.log(len(self.artist_list),2))
        bits_chunks = [binary[i:i+bits] for i in range(0, len(binary), bits)]
        for b in bits_chunks:
            random_track = self.random_track(self.track_list[int(b, 2)])
            self.encode_table.append([random_track[0], self.artist_list[int(b, 2)], str(int(b, 2)), b])
            track_list.append(random_track[1])
        self.add_playlist_tracks(username, playlist_name, track_list)

    def decode_msg(self, username, playlist_name):
        """
        Decodes the message
        """
        binary_msg = ''
        count = 0
        encoded_msg = self.get_playlist_artists(username, playlist_name)
        bits = round(math.log(len(self.artist_list),2))
        for track_artist in progressbar.progressbar(encoded_msg):
            if count == len(encoded_msg)-1 and (len(binary_msg)%bits) != 0:
                last_bits = 8-(len(binary_msg)%8)
                binary_msg = binary_msg + ('{0:0' + str(last_bits) + 'b}').format(self.artist_list.index(track_artist[1]))
                self.encode_table.append([track_artist[0], track_artist[1], str(self.artist_list.index(track_artist[1])), 
                                        ('{0:0' + str(last_bits) + 'b}').format(self.artist_list.index(track_artist[1]))])
            else:
                self.encode_table.append([track_artist[0], track_artist[1], str(self.artist_list.index(track_artist[1])), 
                                        ('{0:0' + str(bits) + 'b}').format(self.artist_list.index(track_artist[1]))])
                binary_msg = binary_msg + ('{0:0' + str(bits) + 'b}').format(self.artist_list.index(track_artist[1]))
            count+=1
        decoded_msg = self.to_str(binary_msg)
        return decoded_msg

    def decode_local_msg(self, username, playlist_name):
        local_table = [["Title", "Artist", "Album"]]
        local_metadata = self.get_playlist_info(username, playlist_name)
        for data in local_metadata:
            local_table.append([data[0], data[1], data[2]])
        return local_table
    
    @staticmethod
    def random_track(track_list):
        rand = secrets.randbelow(len(track_list))
        track = track_list[rand]
        return track

    @staticmethod
    def to_bin(string, delimiter=None):
        """
        String to Binary Conversion
        """
        if delimiter == None:
            return ''.join(format(ord(char), '08b') for char in string)
        elif delimiter == 'space':
            return ' '.join(format(ord(char), '08b') for char in string)

    @staticmethod
    def to_str(bits, delimiter=None):
        """
        Binary to String Conversion
        """
        if delimiter == None:
            chars = []
            for b in range(int(len(bits)/8)):
                byte = bits[b*8:(b+1)*8]
                chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
            return ''.join(chars)
        elif delimiter == 'space':
            return ''.join([chr(int(binary, 2)) for binary in bits.split(' ')])

    @property
    def username(self):
        """
            :returns: username
            :rtype: str
        """
        return self.__username

    @property
    def scope(self):
        """
            :returns: scope
            :rtype: str
        """
        return self.__scope

    @property
    def client_id(self):
        """
            :returns: client_id
            :rtype: str
        """
        return self.__client_id

    @property
    def client_secret(self):
        """
            :returns: client_secret
            :rtype: str
        """
        return self.__client_secret

    @property
    def redirect_uri(self):
        """
            :returns: redirect_uri
            :rtype: str
        """
        return self.__redirect_uri

    @property
    def spotify(self):
        """
            :returns: spotify
            :rtype: str
        """
        return self.__spotify

    @spotify.setter
    def spotify(self, value):
        self.__spotify = value
    
    @property
    def artist_list(self):
        """
            :returns: artist_list
            :rtype: list
        """
        return self.__artist_list
    
    @artist_list.setter
    def artist_list(self, value):
        self.__artist_list.append(value)

    @property
    def track_list(self):
        """
            :returns: track_list
            :rtype: list
        """
        return self.__track_list
    
    @track_list.setter
    def track_list(self, value):
        self.__track_list.append(value)
    
    @property
    def artist_table(self):
        """
            :returns: artist_table
            :rtype: list
        """
        return self.__artist_table
    
    @artist_table.setter
    def artist_table(self, value):
        self.__artist_table.append(value)

    @property
    def track_table(self):
        """
            :returns: track_table
            :rtype: list
        """
        return self.__track_table
    
    @track_table.setter
    def track_table(self, value):
        self.__track_table.append(value)

    @property
    def encode_table(self):
        """
            :returns: encode_table
            :rtype: list
        """
        return self.__encode_table
    
    @encode_table.setter
    def encode_table(self, value):
        self.__encode_table.append(value)
