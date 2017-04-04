import socket
import time
import os
import sys


class Server:

    def __init__(self, port):
        self.host = ''
        self.port = port
        self.dir_list = []
        self.cur_dir = ""

    def activate_server(self):
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))

        self.wait_for_connections()

    def shutdown(self):
        s.socket.shutdown(socket.SHUT_RDWR)

    def gen_headers(self, code):
        h = ''
        if (code == 200):
            h = 'HTTP/1.1 200 OK\n'
        elif (code == 404):
            h = 'HTTP/1.1 404 Not Found\n'

        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        h += 'Date: ' + current_date + '\n'
        h += 'Server: Simple-Python-HTTP-Server\n'
        h += 'Connection: close\n\n'

        return h

    def generate_html(self):
        res = """
                <head>
                    <meta charset="UTF-8">
                    <title>Title</title>
                </head>
                <body>
                <ul>
                    """
        for i in self.dir_list:
            res += "<li>\n<a href=\"" + self.cur_dir + "/" + i + "\">" + i + "</a>\n</li>"
        res += """
                </ul>
                </body>
            """
        return res

    def wait_for_connections(self):

        while True:
            self.socket.listen(1)

            conn, addr = self.socket.accept()

            data = conn.recv(1024)
            string = bytes.decode(data)

            request_method = string.split(' ')[0]

            if (request_method == 'GET') | (request_method == 'HEAD'):
                response_content = ""

                file_requested = string.split(' ')[1]

                file_requested = file_requested.split('?')[0]

                if '/' == file_requested:
                    if os.path.exists('index.html'):
                        file_requested = 'index.html'
                    else:
                        self.dir_list = os.listdir('.')
                        self.cur_dir = ''
                        response_content = self.generate_html()
                else:
                    if "/favicon.ico" == file_requested:
                        continue
                    if os.path.isfile('.' + file_requested):
                        file_requested = '.' + file_requested
                    else:
                        self.dir_list = os.listdir('.' + file_requested)
                        if "index.html" in self.dir_list:
                            file_requested = '.' + file_requested + '/' + "index.html"
                        else:
                            self.cur_dir = file_requested
                            response_content = self.generate_html()


                try:
                    if "" == response_content:
                        file_handler = open(file_requested, 'rb')
                        if request_method == 'GET':
                            response_content = file_handler.read()
                        file_handler.close()
                    else:
                        response_content = response_content.encode('utf-8')

                    response_headers = self.gen_headers(200)
                except Exception as e:
                    response_headers = self.gen_headers(404)

                server_response = response_headers.encode()
                if request_method == 'GET':
                    server_response += response_content

                conn.send(server_response)
                conn.close()

            else:
                print("Unknown HTTP request method:", request_method)


port = int(sys.argv[1])
s = Server(port)
s.activate_server()
