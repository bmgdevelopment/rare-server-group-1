from http.server import BaseHTTPRequestHandler, HTTPServer
from categories import get_single_category, get_all_categories


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
            
            if resource == "categories":
                if id is not None: 
                    response = f"{get_single_category(id)}"
                else: 
                    response = f"{get_all_categories()}"
                    
        self.wfile.write(response.encode())
        
        



def main(): 
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()