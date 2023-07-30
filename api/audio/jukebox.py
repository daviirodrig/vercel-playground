# https://jukebox.davi.gq/api/audio/jukebox/4PYAe64w5zHrhKV4sEWLQx
import contextlib
import io

import ffmpeg
from flask import Flask, Response, request
from rich import print
from yt_dlp import YoutubeDL as yt_dlp
from yt_dlp import utils

app = Flask(__name__)


@app.route("/api/audio/jukebox/", methods=["GET"])
@app.route("/api/audio/jukebox", methods=["GET"])
def get():
    id = request.args.get("id")
    if not id:
        return Response(status=400)
    yt_dlp_config = {
        "extract_flat": "discard_in_playlist",
        "final_ext": "webm",
        "format": "mp3/bestaudio/best",
        "fragment_retries": 10,
        "ignoreerrors": "only_download",
        "max_downloads": 1,
        "max_filesize": 104857600,
        "noplaylist": True,
        "outtmpl": "-",
        "logtostderr": True,
        "playlistend": 1,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "retries": 10,
    }
    buffer = io.BytesIO()

    with contextlib.redirect_stdout(buffer), yt_dlp(yt_dlp_config) as y:
        try:
            y.download(
                f"https://music.youtube.com/search?q={id}&sp=EgWKAQIIAWoKEAoQAxAEEAkQBQ%3D%3D"
            )
        except utils.MaxDownloadsReached:
            pass


    process = (
        ffmpeg.input("pipe:")
        .output(filename="./compress.tmp.mp3", c='libmp3lame', audio_bitrate='128k')
        .run_async(pipe_stdin=True, overwrite_output=True)
    )


    process.communicate(input=buffer.getbuffer())

    with open("./compress.tmp.mp3", "rb") as f:
        ffbuffer = io.BytesIO(f.read())


    print(len(ffbuffer.getvalue()) / 1024)
    return Response(
        ffbuffer.getvalue(),
        mimetype="audio/mp3",
        headers={"Content-Disposition": f"attachment; filename={id}.mp3"},
        direct_passthrough=True,
        status=200,
    )


if __name__ in "__main__":
    app.run(debug=True)
