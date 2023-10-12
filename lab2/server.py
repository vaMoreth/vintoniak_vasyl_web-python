from http.server import  HTTPServer, CGIHTTPRequestHandler
adders = ("localhost", 5050)

server = HTTPServer(adders, CGIHTTPRequestHandler)
print("Listenint...")
server.serve_forever()