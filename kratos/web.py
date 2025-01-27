from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import kratoslib

hostname = '0.0.0.0'
serverPort = 5000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == '/':
            self.do_Index()
            return

        if  "/snap.png" in self.path:
            self.do_Snap()
            return

        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return

    def do_Index(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('html/index.html', 'r') as f:
            self.wfile.write(bytes(f.read(), 'utf-8'))
        return


    def do_Snap(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        print("Getting snapshot")
        image = requests.get('https://aezstoprdhandelsvegg.z6.web.core.windows.net/snap.png')
        #image = requests.get('https://aezstoprdhvegg.z16.web.core.windows.net/snap.png')
        self.wfile.write(image.content)
        return


if __name__ == "__main__":
    webServer = HTTPServer((hostname, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostname, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass


    webServer.server_close()
    print("Server stopped")
