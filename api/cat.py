from http.server import BaseHTTPRequestHandler
from datetime import datetime
from deta import Deta
from PIL import Image
import os
import io


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "image/jpeg")
        self.end_headers()

        # get query parameters froms self.path
        query_string = self.path.split("?")
        if len(query_string) > 1:
            query_params = query_string[1].split("&")
            query_dict = {}
            for q in query_params:
                key, value = q.split("=")
                query_dict[key] = value
        else:
            query_dict = {}


        cat_img = self.get_image("2023-04-18-02-41-39cat.jpeg")

        if "r" in query_dict:
            if cat_img != None:
                resized_cat_img = self.resize_image(
                    cat_img.read(), int(query_dict["r"])
                )
                self.wfile.write(resized_cat_img)
            return

        if cat_img != None:
            self.wfile.write(cat_img.read())
        return

    @staticmethod
    def resize_image(image_bytes: bytes, size: int) -> bytes:
        pil_image = Image.open(io.BytesIO(image_bytes))

        if pil_image.size[0] < size or pil_image.size[1] < size:
            return image_bytes

        pil_image = pil_image.resize((size, size))

        bytes_res = io.BytesIO()
        pil_image.save(bytes_res, format="JPEG")

        return bytes_res.getvalue()

    @staticmethod
    def get_image(img_name: str):
        deta = Deta(os.environ["DETA_PROJECT_KEY"])
        drive = deta.Drive("drivefoda")

        def upload_cat():
            # Upload cat image to drive
            with open("cat.jpeg", "rb") as f:
                fileNameWithTimestamp = (
                    datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + "cat.jpeg"
                )
                drive.put(fileNameWithTimestamp, f)
                print("Uploaded cat.jpeg")
                return drive.get(fileNameWithTimestamp)

        res = drive.get(img_name)
        return res
