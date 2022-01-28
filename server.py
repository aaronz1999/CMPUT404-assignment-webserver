#  coding: utf-8 
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))
        decoded_data = self.data.decode('utf-8').split()
        requested_path = decoded_data[1]
        method = decoded_data[0]
        #print(decoded_data)
        #check if method is get, and execute if it is
        if method == 'GET':
            #handling test case
            if "/." or "/.." in requested_path:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
            else:
                my_path = os.path.join(os.getcwd()+'/www' + requested_path)
                #handle if the requested end with a file or a directory
                if os.path.isfile(my_path):
                    #handle html and css files, return 404 if file invalid
                    if ".html" in requested_path:
                        f = open(my_path)
                        file = f.read()
                        self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n{file}",'utf-8'))
                        f.close()
                    elif ".css" in requested_path:
                        f = open(my_path)
                        file = f.read()
                        self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\ncontent-type: text/css\r\n\r\n{file}",'utf-8'))
                        f.close()
                    else:
                        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                elif os.path.isdir(my_path):
                    #301 redirect if / does not present in end of path, handle otherwise
                    if not my_path.endswith("/"):
                        change_path = requested_path + '/'
                        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: http://127.0.0.1:8080%s\r\n" % (change_path), 'utf-8'))
                    else:
                        change_path = requested_path + "index.html"
                        new_path = os.path.join(os.getcwd()+'/www' + change_path)
                        f = open(new_path)
                        file = f.read()
                        self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n{file}",'utf-8'))
                        f.close()
                #return 404 if no file or directory found
                else:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
        #return 405 if method is not get
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            





if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
