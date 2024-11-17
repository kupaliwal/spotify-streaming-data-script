import json

input_files = [ 'StreamingHistory_music_0.json',    #these are all the streaming history files, change as needed
                'StreamingHistory_music_1.json',
                'StreamingHistory_music_2.json',
                'StreamingHistory_music_3.json',
                'StreamingHistory_music_4.json',
                'StreamingHistory_music_5.json',
                'StreamingHistory_music_6.json'
]

aggregate_data = {}   #dictionary for all the data

def getting_info(input_files):
    for input_file in input_files:

        with open(input_file, 'r') as file:               # opens the input files in read mode
            data = json.load(file)
    

        for entry in data:                                 # this gets all the data on tracks and ms played
            artist = entry.get('artistName', 'unknown')
            track = entry.get('trackName', 'unknown')
            ms_played = entry.get('msPlayed', 0)
        
            key = (artist, track)


            if key in aggregate_data:
                aggregate_data[key] += ms_played
            else:
                aggregate_data[key] = ms_played

        with open('output.json', 'w') as output_file:      # opens the output json with all the songs and their time
            output_data = []  

            total_time = 0                  
            total_songs = 0

            top_artists = {}
            for (artist, track), total_ms_played in aggregate_data.items():
                min_played = round(total_ms_played / 60000, 2)         #converts to minutes, rounds to 2 decimal places
                output_data.append({                                   # format for the json
                    "Name": artist,     
                    "Song": track,
                    "Minutes Played": min_played
                })
                
                total_time += min_played                                    # calculates total time spend listening to music
                total_songs += 1                                            # calculates the total number of songs

                if artist in top_artists:
                    top_artists[artist] += min_played
                else:
                    top_artists[artist] = min_played
            output_data = sorted(output_data, key=lambda x: x['Minutes Played'], reverse=True)          #sorts by highest number first

            sorted_artists = sorted(top_artists.items(), key=lambda x: x[1], reverse=True)              # sorts top artists
            top_5_artists = sorted_artists[:5]                                                          # the :5 means it gives the first 5 

            json.dump(output_data, output_file, indent=4, ensure_ascii=False)                           # writes out the song information to output.json

        with open('total_time.json', 'w') as total_time_file:                                           # opens file for total time listening, total songs listened, and top 5 artists listened to 
            
            json.dump({"Total Time": round(total_time, 2), "Total Songs": total_songs, "Top 5 Artist": top_5_artists}, total_time_file, indent=4)    # writes that information


getting_info(input_files)        # calls the actual function 




