from multiprocessing import Process
from multiprocessing import Pipe
from flask import Flask, render_template
import SocketServer
import socket
import time
import select
import signal
import sys

a, b = Pipe()

def webSvr():

  print ('starting Flask server')

  app = Flask(__name__)

  @app.route('/bot')
  def index():
    return render_template('index.html')

  @app.route('/forward/')
  def forward():
    a.send('8')
    print ('sombody clicked forward!!')
    return render_template('index.html')


  @app.route('/reverse/')
  def reverse():
    a.send('2')
    print ('sombody clicked reverse!')
    return render_template('index.html')

  @app.route('/left/')
  def left():
    a.send('4')
    print ('sombody clicked left!')
    return render_template('index.html')

  @app.route('/stop/')
  def stop():
    a.send('5')
    print ('sombody clicked stop!')
    return render_template('index.html')

  @app.route('/right/')
  def right():
    a.send('6')
    print ('sombody clicked right!')
    return render_template('index.html')

  @app.route('/exit/')
  def exit():
    a.send('exit')
    print ('sombody clicked exit!')
    return render_template('index.html')

  app.run(debug=False, host = '0.0.0.0', port=5000)
  
def socSvr():
  restarts = 0
  allowedRestarts = 0
  while restarts <= allowedRestarts:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "starting socSvr, restarts: %s" % restarts
    s.setblocking(0)
    s.bind(("",23000))
    s.listen(1)
    while 1:
      try:
        conn, addr = s.accept()
      except:
        print "no incoming connection"
        time.sleep(2)
      else:
        print "socSvr connected by ", addr
        command = (b.recv())
        conn.sendall(command)
        while 1:
          try:
            response = conn.recv(8)
          except:
            print "no response from robot"
            time.sleep(2)
          else:
            print "robot responded: %s" % response
            break
    conn.close()
    restarts = restarts + 1
  print "socSvr allowed restarts exceeded. not restarting socSvr"
    
    

"""
def socSvr():
  print('starting socket server')
  class MyTCPHandler( SocketServer.BaseRequestHandler ):
    def handle( self ):
      print ('connected to robot')
      self.allow_reuse_address = True
      self.request.sendall("Hello Robot!\n")
      while 1:
        command  = (b.recv())
        print "botSvrThread received command from webSvrThread: %s" % (command)
        if command == 'exit':
          server_close()
          break
        self.request.sendall(command)
        print "botSvrThread send command to robot: %s" % (command)
        self.data = self.request.recv(8).strip()
        print "{} robot responded:".format(self.client_address[0])
        print self.data
        
  server = SocketServer.TCPServer( ("", 23000), MyTCPHandler )
  server.serve_forever()
  #server.handle_request()
  #server.timeout(10)
"""
  
"""
        print "this is the line before self.rfile.read"
        response = "."
        response = self.rfile.read(8)
        print "this is the line after self.rfile.read"
        if response == "received":
          print "robot acknowledged response"
        else:
          print "robot did not acknowlege response"
      
      self.wfile.write('Goodbye Robot!\n"')
      self.allow_reuse_address = True
"""


def robotCmd():
  print ('robotCmd called')
  global command
  while 1:
    print (command)
    command = (b.recv())
    print (command)
    time.sleep(1)
    
"""
def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)
            server_close()

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)
"""

x = 1

global command
global response
command = "."
response = "."



if __name__ == '__main__':
#  original_sigint = signal.getsignal(signal.SIGINT)
#  signal.signal(signal.SIGINT, exit_gracefully)
  Process(target=webSvr).start()  #start flask and serve up control page to human
  Process(target=socSvr).start()  #start socketServer to send commands to robot


  
  
  
  
