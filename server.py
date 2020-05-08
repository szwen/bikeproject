import http.server
import socketserver
import sys
import realtime_frequency as rpm
import threading


thread1 = threading.Thread(target = rpm.main)

def return_index():
  file = open('index.html')
  return file.read()

def getHello(handler):
  handler.send_header('Content-type', 'text/html')
  handler.end_headers()
  message = bytes(return_index(), 'utf-8')
  handler.wfile.write(message)

def getBye(handler):
  handler.send_header('Content-type', 'text/plain')
  handler.end_headers()
  message = bytes('Bye', 'utf-8')
  handler.wfile.write(message)

def startService(handler):
  handler.send_header('Content-type', 'text/plain')
  handler.end_headers()
  message = bytes('service started!', 'utf-8')
  handler.wfile.write(message)
  thread1.start()

def getRpm(handler):
  handler.send_header('Content-type', 'text/plain')
  handler.end_headers()
  message = bytes(str(100), 'utf-8')

def stopService(handler):
  handler.send_header('Content-type', 'text/plain')
  handler.end_headers()
  message = bytes('service stopped!', 'utf-8')
  handler.wfile.write(message)


class MyRequestHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    handler = self
    print('Receiving request for path ' + str(self.path))
    if self.path == '/hello' or self.path=='/':
      self.send_response(200)
      getHello(self)
      print('Sending resource to '+ str(self.client_address))
    elif self.path == '/bye':
      self.send_response(200)
      getBye(self)
    elif self.path == '/start':
      self.send_response(200)
      startService(self)
    elif self.path == '/stop':
      self.send_response(200)
      stopService(self)
    elif self.path=='/rpm':
      self.send_response(200)
      print('Getting rpm')
      getRpm(self)
    else:
      self.send_response(404)
    return

def run(server_class, handler_class):
  server_address = ('', int(sys.argv[1]))
  httpd = server_class(server_address, handler_class)
  httpd.serve_forever()

def main():
  print('Server started in port '+sys.argv[1])
  run(http.server.ThreadingHTTPServer, MyRequestHandler)

if __name__ == "__main__":
  main()
