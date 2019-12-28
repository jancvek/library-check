from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading

from os import curdir, sep
import json

import os

currPath = os.path.dirname(os.path.abspath(__file__))
parentPath = os.path.dirname(currPath)
libPath = parentPath+'/jan-lib'

# tole moramo dodati da lahko importamo py file iz drugih lokacij
import sys
sys.path.insert(1, libPath)

import jan_sqlite
import library
import library_service

PORT = 8080

class Handler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):

        # print(self.path)
        # rootdir = 'c:/xampp/htdocs/' #file location  
        try:  
            # if self.path.endswith('.html'): 
            if self.path.endswith('/'):   
                print("v defaultnem pathu")
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

                # data_list = []

                # conn = jan_sqlite.create_connection(r"data.db")
                # with conn:
                #     rows = jan_sqlite.get_data_all(conn)

                #     for row in rows:
                #         d = {
                #             "id": row[0],
                #             "text": row[1]
                #         }
                #         data_list.append(d)


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
                # mStr = json.dumps(data_list)
                mStr = json.dumps({"test":"dela"})
                mBin = mStr.encode('utf-8')

                self.wfile.write(mBin)

            elif self.path.endswith('/knj'):
                print("v kniznica pathu")

                #open requested file
                f = open(currPath + sep +"knjiznica.html")   

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

            elif self.path.endswith('/knjApi/main'):
                #send code 200 response  
                self.send_response(200)

                #send header first  
                self.send_header('Content-type', 'application/json')
                self.end_headers()    

                resJson = library.getLibraryMain()

                mStr = json.dumps(resJson)
                mBin = mStr.encode('utf-8')

                self.wfile.write(mBin) 
            
            elif self.path.endswith('/knjApi/checkLib'):

                library_service.checkLibrary()
                
                #send code 200 response  
                self.send_response(200)

                self.send_header('Content-type', 'application/json')
                self.end_headers()    

                mStr = json.dumps({"status": "OK"})
                mBin = mStr.encode('utf-8')

                self.wfile.write(mBin) 

        except IOError:  
            self.send_error(404, 'file not found')  

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', PORT), Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()