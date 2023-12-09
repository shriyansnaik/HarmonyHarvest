from app import app
from flask import render_template, request, jsonify


def yt_dlp_download(filename, url):
    from yt_dlp import YoutubeDL
    params = {"outtmpl": f"songs/{filename}", "format": "mp4"}
    with YoutubeDL(params) as ydl:
        ydl.download(url)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/download-my-songs", methods=['POST'])
def download_my_songs():
    # yt_dlp_download(URLS)
    download_data = request.json['data']
    # print(download_data)
    total_songs, successful, failed = 0, 0, 0
    failed_songs = []
    for song_data in download_data:
        if 'link' not in song_data or 'singer' not in song_data or 'song' not in song_data:
            continue
        singer_name, song_name = song_data['singer'].strip(
        ), song_data['song'].strip()
        singer_name = singer_name.lower().replace("dr","").strip()
        filename = f"{singer_name}-{song_name}.mp4"

        url = song_data['link'].strip()
        if not singer_name or not song_name or not url:
            continue
        total_songs += 1
        try:
            yt_dlp_download(filename, url)
            successful += 1
        except Exception as e:
            failed += 1
            failed_songs.append({'song': filename, 'reason': e.args[0][18:]})

    res = {'total_songs': total_songs, 'downloaded': successful,
           'failed': failed, 'failed_songs': failed_songs}

    return res
