from typing import Union
from fastapi import FastAPI, Response
from a2wsgi import ASGIMiddleware
from api.utils import resize_image, get_image

app = FastAPI()


@app.get("/api/fastapiCat")
def read_root(r: int = 1024):
    cat_img = get_image("2023-04-18-02-41-39cat.jpeg")

    if cat_img == None:
        return "cat_img is None"

    if r < 1024:
        resized = resize_image(image_bytes=cat_img.read(), size=r)
        return Response(content=resized, media_type="image/jpeg")

    return Response(content=cat_img.read(), media_type="image/jpeg")


app = ASGIMiddleware(app)
