import os
import subprocess
import yt_dlp

# Path to ffmpeg (this is a portable version i included so users don't have to install
# this by themselves, can be found as full build in ffmpeg webpage)
def get_ffmpeg_path():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, 'ffmpeg', 'bin', 'ffmpeg.exe')

def run_ffmpeg(input_file, output_file):
    ffmpeg_path = get_ffmpeg_path()
    command = [ffmpeg_path, '-i', input_file, output_file]
    subprocess.run(command)

# File containing the list of songs (either URLs or search query)
# I included an example file in the executable version of this
SONG_LIST_FILE = 'songs.txt'

# YouTube download options for the best available quality
# All settings can be changed, I setted this up for my usecase
ydl_opts = {
    'format': 'bestaudio/best',                          # Select best audio format available
    'outtmpl': '%(title)s.%(ext)s',                      # Output filename: audio title
    'noplaylist': True,                                  # Avoid downloading playlists
    'postprocessors': [{                                 # Convert audio to MP3 after download
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',                         # Convert to MP3
        'preferredquality': '192',                       # Set audio quality (192 kbps)
    }],
    'ffmpeg_location': get_ffmpeg_path(),                # Specify custom ffmpeg location
}

def download_song(song_name):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f"ytsearch:{song_name}"])  # Search and download the first result (this means you need to provide a good query)
        except Exception as e:
            print(f"Failed to download {song_name}: {e}")


def main():
    
    # Read the list of songs
    with open(SONG_LIST_FILE, 'r') as f:
        songs = [line.strip() for line in f if line.strip()]
    
    # Download each song
    for song in songs:
        print(f"Downloading {song} as MP3...")
        download_song(song)

if __name__ == '__main__':
    main()
