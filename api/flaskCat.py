from flask import Flask, request, Response

from api.utils import get_image, resize_image

app = Flask(__name__)


@app.route("/api/flaskCat")
def home():
    r = request.args.get("r")
    cat_img = get_image("2023-04-18-02-41-39cat.jpeg")

    if cat_img == None:
        return "cat_img is None"

    if r != None and int(r) < 1024:
        resized = resize_image(image_bytes=cat_img.read(), size=int(r))
        return Response(response=resized, content_type="image/jpeg")

    return Response(response=cat_img.read(), content_type="image/jpeg")
