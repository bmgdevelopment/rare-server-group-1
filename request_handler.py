from http.server import BaseHTTPRequestHandler, HTTPServer
from categories import get_single_category, get_all_categories, create_category
from users import (create_user, get_all_users, get_single_user, get_user_by_email)
from subscriptions import (get_all_subscriptions, get_single_subscription, get_subscription_by_author_id, create_subscription)

import json

class HandleRequests(BaseHTTPRequestHandler):
    
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
        
        if "?" in resource: 
            
            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
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
            
            return ( resource, id )

  # Here's a class function
    def _set_headers(self, status): 
        self.send_response(status) 
        self.send_header('Content-type', 'application/json') 
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers() 

    # Another method! This supports requests with the OPTIONS verb.
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
            
            if resource == "users":
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
              
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            if key == "email" and resource == "users":
                response = get_user_by_email(value)
                
            elif key == "author_id" and resource == "subscriptions":
                response = get_subscription_by_author_id(value)
            
                      
        self.wfile.write(response.encode())
        
        
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        
        post_body = json.loads(post_body)
        
        (resource, id) = self.parse_url(self.path)
        
        new_user = None

        if resource == "users":
            new_user = create_user(post_body)
            self.wfile.write(f"{new_user}".encode())
        
        new_category = None
        
        if resource == "categories":
            new_category = create_category(post_body)            
            self.wfile.write(f"{new_category}".encode())

        new_subscription = None
        
        
        if resource == "subscriptions":
            new_subscription = create_subscription(post_body)
            self.wfile.write(f"{new_subscription}".encode())

def main(): 
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()
    
