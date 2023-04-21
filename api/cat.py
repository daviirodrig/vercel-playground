from http.server import BaseHTTPRequestHandler
from api.utils import get_image, resize_image

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


        cat_img = get_image("2023-04-18-02-41-39cat.jpeg")

        if "r" in query_dict:
            if cat_img != None:
                resized_cat_img = resize_image(
                    cat_img.read(), int(query_dict["r"])
                )
                self.wfile.write(resized_cat_img)
            return

        if cat_img != None:
            self.wfile.write(cat_img.read())
        return
