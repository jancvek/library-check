import http.server
import socketserver
from os import curdir, sep
import json
import jan_sqlite

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

class myHandler(Handler):

    #Handler for the GET requests
    def do_GET(self):

        # rootdir = 'c:/xampp/htdocs/' #file location  
        try:  
            # if self.path.endswith('.html'): 
            if self.path.endswith('/'):   
                print(self.path)
                self.path = "index.html"
                f = open(curdir + sep +self.path) #open requested file  
        
                #send code 200 response  
                self.send_response(200)  
        
                #send header first  
                self.send_header('Content-type','text-html')  
                self.end_headers()  
        
                #send file content to client  
                fileData = f.read()
                self.wfile.write(fileData.encode('utf-8'))  
                f.close()  
                return

            elif self.path.endswith('/api/test'):
                self.send_response(200)
                # self.send_header('Content-type','text/html')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                # Send the html message
                # self.wfile.write(b'Hello, world!')

                data_list = []

                conn = jan_sqlite.create_connection(r"data.db")
                with conn:
                    rows = jan_sqlite.get_data_all(conn)

                    for row in rows:
                        d = {
                            "id": row[0],
                            "text": row[1]
                        }
                        data_list.append(d)


                # data_list = []
                
                # mes1 = {
                #     "name": "John",
                #     "age": 30
                # }
                # mes2 = {
                #     "name": "Ana",
                #     "age": 22
                # }

                # data_list.append(mes1)
                # data_list.append(mes2)

                # mStr = json.dumps(message)
                mStr = json.dumps(data_list)
                mBin = mStr.encode('utf-8')

                self.wfile.write(mBin)

        except IOError:  
            self.send_error(404, 'file not found')  


with socketserver.TCPServer(("", PORT), myHandler) as httpd:
    try:
        print("serving at port", PORT)
        httpd.serve_forever()
    except Exception:
        httpd.shutdown()