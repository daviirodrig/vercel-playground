import os
import io
from deta import Deta
from datetime import datetime
from PIL import Image


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


def resize_image(image_bytes: bytes, size: int) -> bytes:
    pil_image = Image.open(io.BytesIO(image_bytes))

    if pil_image.size[0] < size or pil_image.size[1] < size:
        return image_bytes

    pil_image = pil_image.resize((size, size))

    bytes_res = io.BytesIO()
    pil_image.save(bytes_res, format="JPEG")

    return bytes_res.getvalue()
