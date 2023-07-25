# https://jukebox.davi.gq/api/audio/jukebox/4PYAe64w5zHrhKV4sEWLQx
import contextlib
import io

from flask import Flask, Response, request
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
        "format": "bestaudio/best",
        "fragment_retries": 10,
        "ignoreerrors": "only_download",
        "max_downloads": 1,
        "max_filesize": 104857600,
        "noplaylist": True,
        "outtmpl": "-",
        "logtostderr": True,
        "playlistend": 1,
        # "postprocessors": [
        #     {
        #         "key": "FFmpegExtractAudio",
        #         "nopostoverwrites": False,
        #         "preferredcodec": "m4a",
        #         "preferredquality": "5",
        #     },
        #     {"key": "FFmpegConcat", "only_multi_video": True, "when": "playlist"},
        # ],
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

    return Response(
        buffer.getvalue(),
        mimetype="audio/webm",
        headers={"Content-Disposition": f"attachment; filename={id}.webm"},
        direct_passthrough=True,
        status=200,
    )


if __name__ in "__main__":
    app.run(debug=True)
