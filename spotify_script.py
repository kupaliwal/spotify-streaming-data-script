import json

input_files = [ 'StreamingHistory_music_0.json',    #these are all the streaming history files, change as needed
                'StreamingHistory_music_1.json',
                'StreamingHistory_music_2.json',
                'StreamingHistory_music_3.json',
                'StreamingHistory_music_4.json',
                'StreamingHistory_music_5.json',
                'StreamingHistory_music_6.json'
]

aggregate_data = {}                                 #dictionary for all the data

def getting_info(input_files):
    combined_data = []                              # List to hold data from all files
    for input_file in input_files:
        with open(input_file, 'r') as file:         # Open each file in read mode
            data = json.load(file)                  # Load JSON data from the file
            if isinstance(data, list):              # Ensure the file contains a list of entries
                combined_data.extend(data)  
    return combined_data

        
def reading_info(combined_data):
    for entry in combined_data:              
        artist = entry.get('artistName', 'unknown')
        track = entry.get('trackName', 'unknown')
        ms_played = entry.get('msPlayed', 0)
        
        key = (artist, track)

        if key in aggregate_data:
            aggregate_data[key] += ms_played
        else:
            aggregate_data[key] = ms_played
    return aggregate_data


def write_song_info(aggregate_data):
    with open('output.json', 'w') as output_file:    
        #opens output.json in writing mode
        
        output_data = []  
        total_time = 0                  
        total_songs = 0
        top_artists = {}

        for (artist, track), total_ms_played in aggregate_data.items():
            min_played = round(total_ms_played / 60000, 2)  # converts ms to minutes, rounded to 2 decimal places
            
            # Add song info to the output_data
            output_data.append({
                "Name": artist,     
                "Song": track,
                "Minutes Played": min_played
            })

            # Accumulate total time and total songs
            total_time += min_played
            total_songs += 1

            # Accumulate artist's total play time in top_artists
            if artist in top_artists:
                top_artists[artist] += min_played
            else:
                top_artists[artist] = min_played

        # Sort the songs by 'Minutes Played' in descending order
        output_data = sorted(output_data, key=lambda x: x['Minutes Played'], reverse=True)
        
        # Write the song info to output.json
        json.dump(output_data, output_file, indent=4, ensure_ascii=False)
        
        return total_time, total_songs, top_artists


def write_total_time(total_time, total_songs, top_artists):
    #writes down the total time and other info for your "wrapped"
    with open('wrapped.json', 'w') as total_time_file:                                          
        

        sorted_artists = sorted(top_artists.items(), key=lambda x: x[1], reverse=True)           
        top_5_artists = sorted_artists[:5] 

        json.dump({"Total Time": round(total_time, 2),
                    "Total Songs": total_songs, 
                    "Top 5 Artist": top_5_artists
                    }, total_time_file, indent=4)    



def main_func(input_files):
    #main function, calls all the other ones
    combined_data = getting_info(input_files)
    aggregate_data = reading_info(combined_data)
    total_time, total_songs, top_artists = write_song_info(aggregate_data)
    write_total_time(total_time, total_songs, top_artists)
    


#runs the main function
main_func(input_files)
