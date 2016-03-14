import plistlib
import pprint
import logging

log_file = "/Users/Dave/Scripts/Playlists/import_old.log"

logging.basicConfig(filename=log_file, level=logging.INFO)

# Old Library
Old_Library = plistlib.readPlist('')
# Old track list and playlists
old_tracks = Old_Library['Tracks']
playlists = Old_Library['Playlists']

# New Library
New_Library = plistlib.readPlist('')
# New track list
new_tracks = New_Library['Tracks']

# Structure of new_tracks:
# {
#   track_ID:
#   {
#       Album
#       Artist
#       ...etc...
#   }
#}

# Set up dictionaries etc.
songs_in_lists = {}
possible_songs = []
new_playlist_items = {}
new_playlists = {}

# Find all the Track IDs for songs in playlists

# Unwanted Playlists
unwanted_playlists = ["Library", "TV Shows", "Podcasts", "Movies", "Music", "Audiobooks", "iTunes U", "Quicksilver"]

for playlist in playlists:
    if type(playlist["Name"]) == unicode:
        playlist_name = playlist["Name"].replace(u'\u2019', '\'').replace(u'\xa0', ' ').encode('utf-8')
    else:
        playlist_name = playlist["Name"]
    
    if playlist_name not in unwanted_playlists and "Smart Criteria" not in playlist.keys():
        # Add the playlist to the new playlist dictionary if it's not been added already:
        if playlist_name not in new_playlists:
            new_playlists[playlist_name] = {}
            logging.info("Created a new playlist: " + playlist_name)
        
        # construct a dictionary for the old information for each song in the playlist
        songs_in_lists[playlist_name] = {}
        if "Playlist Items" in playlist.keys():
            for playlist_items in playlist["Playlist Items"]:
                for keys, IDs in playlist_items.items():
                    songs_in_lists[playlist_name][IDs] = {}

# Find the name of the songs in the playlists
for playlist, songs in songs_in_lists.items():
    for ID, names in songs.items():
        # Catch exceptions from missing keys
        try:
            songs_in_lists[playlist][ID]["Name"] = old_tracks[str(ID)]["Name"]
        except:
            songs_in_lists[playlist][ID]["Name"] = "Untitled"
        try:
            songs_in_lists[playlist][ID]["Album"] = old_tracks[str(ID)]["Album"]
        except:
            songs_in_lists[playlist][ID]["Album"] = "<No Album>"
        try:
            songs_in_lists[playlist][ID]["Total Time"] = old_tracks[str(ID)]["Total Time"]
        except:
            # If the song hasn't got a total time, something's gone wrong;
            # this is set by iTunes without human interaction
            pass

pp = pprint.PrettyPrinter(indent=4)

# Structure of songs_in_lists (songs_in_lists is a dictionary):
# { Playlist Name:
#   {
#       Track_ID:
#       {
#           Album: Track Album Name
#           Name: Track Name
#           Total Time: Length of the track, used for matching purposes
#       }
#    }
# }

# Need to pick out the tracks from the current library which are in the old playlists.

for new_track_ID, new_track_info in new_tracks.items():
    # This level is looping over each individual track in the new library
    for playlist, tracks in songs_in_lists.items():
        # now we loop over each playlist...
        for old_track_ID, old_track_info in tracks.items():
            # and each track in that playlist:
            try:
                if (new_track_info['Album'] == old_track_info['Album']) and (new_track_info['Name'] == old_track_info['Name']) and (old_track_info['Total Time'] == old_track_info['Total Time']):
                    logging.info("Found new track: " + new_track_info['Name'] + " from the album: " + new_track_info['Album'])
                    logging.info("Adding info to the playlist dictionary:")
                    new_playlists[playlist][new_track_ID] = new_track_info
                    logging.info(new_playlists[playlist][new_track_ID])
            except KeyError:
                pass
    
pp.pprint(new_playlists)