import http.server
import socketserver
import sys
import realtime_frequency as rpm
import threading
import queue

stop_thread = False
global thread1 
#= threading.Thread(target = rpm.main, args =(lambda : stop_thread, ))
global main_queue
rpm_to_return = 'No value'



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
  global thread1
  global stop_thread
  stop_thread = False
  global main_queue
  main_queue = queue.Queue()
  handler.send_header('Content-type', 'text/plain')
  handler.end_headers()
  message = bytes('service started!', 'utf-8')
  handler.wfile.write(message)
  try:
    thread1 = threading.Thread(target = rpm.main, args =(lambda : stop_thread, main_queue))
    thread1.start()
  except RuntimeError:
    print('thread was already started')
    pass

def getRpm(handler):
  handler.send_header('Content-type', 'text/plain')
  handler.end_headers()
  global rpm_to_return
  if not main_queue.empty():
    rpm_to_return = str(main_queue.get())
  else:
    pass    
  print("Returning rpm: "+ rpm_to_return)
  message = bytes(rpm_to_return, 'utf-8')
  handler.wfile.write(message)

def stopService(handler):
  global stop_thread
  global thread_1
  stop_thread = True
  thread1.join() 
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
