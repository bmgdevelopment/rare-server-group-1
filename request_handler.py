from http.server import BaseHTTPRequestHandler, HTTPServer
from categories import get_single_category, get_all_categories, create_category
from posts.request import get_post_by_title
from users import (create_user, get_all_users, get_single_user, get_user_by_email, login_user)
from posts import( 
get_all_posts,
get_single_post,
create_post,
delete_post,
update_post
)
import json

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


        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            if key == "email" and resource == "users":
                response = get_user_by_email(value)

            if key == "title" and resource == "posts":
                response = get_post_by_title(value)

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
        new_post = None
        new_category = None
      
        if resource == "categories":
           new_category = create_category(post_body)           
           self.wfile.write(f"{new_category}".encode())
 
        
        if resource == "posts":
            new_post = create_post(post_body)
            
            self.wfile.write(f"{new_post}".encode())
            
        self.wfile.write(json.dumps(response).encode())
        
        
def do_DELETE(self):
        self._set_headers(204)
        
        (resource, id) = self.parse_url(self.path)   
        
        if resource == "employees":
            delete_post(id) 
            
        self.wfile.write("".encode())
        
        
def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        
        (resource, id) = self.parse_url(self.path)
        
        success = False
        
        if resource == "posts":
            success = update_post(id, post_body)
            
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
            
        self.wfile.write("".encode())


def main():
    host = ''
    port = 8088
    print(f'listening on port {port}!')
    HTTPServer((host, port), RareRequestHandler).serve_forever()


if __name__ == "__main__":
    main()