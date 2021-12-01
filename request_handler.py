from http.server import BaseHTTPRequestHandler, HTTPServer
from subscriptions import (get_all_subscriptions, get_single_subscription, get_subscription_by_author_id, create_subscription)
import json
from comments import get_all_comments, get_single_comment
from categories import get_single_category, get_all_categories, create_category, update_category, delete_category
from users import (create_user, get_all_users, get_single_user, get_user_by_email, login_user)
from posts import (create_post, get_all_posts, get_single_post, delete_post, update_post)
from tags import get_all_tags, get_single_tag, create_tag, update_tag, delete_tag

class RareRequestHandler(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split('/')
        resource = path_params[1]

        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]

            return ( resource, key, value )

        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

        return (resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)
        response = {}
        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
            elif resource == "users":
                if id is not None:
                    response = f'{get_single_user(id)}'
                else:
                    response = f'{get_all_users()}'
            elif resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
            elif resource == "subscriptions":
                if id is not None:
                    response = f"{get_single_subscription(id)}"
                else:
                    response = f"{get_all_subscriptions()}"
            elif resource == "tags":
                if id is not None:
                    response = f"{get_single_tag(id)}"
                else:
                    response = f"{get_all_tags()}"
            elif resource == "comments":
                if id is not None:
                    response = f"{get_single_comment(id)}"
                else:
                    response = f"{get_all_comments()}"


        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            if key == "email" and resource == "users":
                response = get_user_by_email(value)


            elif key == "author_id" and resource == "subscriptions":
                response = get_subscription_by_author_id(value)


        self.wfile.write(response.encode())


    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        raw_body = self.rfile.read(content_len)
        post_body = json.loads(raw_body)
        (resource, id) = self.parse_url(self.path)


        response = None

        if self.path == '/login':
            user = login_user(post_body)
            if user:
                response = {
                    'valid': True,
                    'token': user.id
                }
                self._set_headers(200)
            else:
                response = { 'valid': False }
                self._set_headers(404)
                self.wfile.write(json.dumps(response).encode())

        if self.path == '/register':
            try:
                new_user = create_user(post_body)
                response = {
                    'valid': True,
                    'token': new_user.id
                }
            except Exception as e:
                response = {
                    'valid': False,
                    'error': str(e)
                }
            self._set_headers(201)
            self.wfile.write(json.dumps(response).encode())


        # CREATE NEW CATEGORY
        new_category = None

        if resource == "categories":
            new_category = create_category(post_body)
            self._set_headers(201)
            self.wfile.write(f"{new_category}".encode())

        new_post = None

        if resource == "posts":
            new_post = create_post(post_body)
            self._set_headers(201)
            self.wfile.write(f"{new_post}".encode())

        # CREATE NEW TAG
        new_tag = None

        if resource == "tags":
            new_category = create_tag(post_body)
            self.wfile.write(f"{new_tag}".encode())


        new_subscription = None


        if resource == "subscriptions":
            new_subscription = create_subscription(post_body)
            self._set_headers(201)
            self.wfile.write(f"{new_subscription}".encode())


    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "categories":
            success = update_category(id, post_body)
        # rest of the elif's
        elif resource == "posts":
            success = update_post(id, post_body)

        elif resource == "tags":
            success = update_tag(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())



    def do_DELETE(self):
    # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # DELETE ONE CATEGORY
        # ------------------
        # Delete a single category from the list
        if resource == "categories":
            delete_category(id)

        if resource == "posts":
            delete_post(id)
        # DELETE ONE TAG
        # ------------------
        # Delete a single tag from the list
        if resource == "tags":
            delete_tag(id)

        # Encode the new category and send in response
            self.wfile.write("".encode())



def main():
    host = ''
    port = 8088
    print(f'listening on port {port}!')
    HTTPServer((host, port), RareRequestHandler).serve_forever()


if __name__ == "__main__":
    main()