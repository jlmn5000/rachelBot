from multiprocessing import Process
from multiprocessing import Pipe
from flask import Flask, render_template
import SocketServer
import time

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
  print('starting socket server')
  class hwRequestHandler( SocketServer.StreamRequestHandler ):
    def handle( self ):
      print ('connected to robot')
      self.wfile.write("Hello Robot!\n")
      while 1:
        command  = (b.recv())
        print (command)
        if command == 'exit':
          break
        else:
          self.wfile.write(command)
          
      self.wfile.write('Goodbye Robot!\n"')
      #self.allow_reuse_address = True

  server = SocketServer.TCPServer( ("", 23000), hwRequestHandler )
  server.serve_forever()

def robotCmd():
  print ('robotCmd called')
  global command
  while 1:
    print (command)
    command = (b.recv())
    print (command)
    time.sleep(1)
    

x = 1

global command
command = "."



if __name__ == '__main__':
  Process(target=webSvr).start()  #start flask and serve up control page to human
  Process(target=socSvr).start()  #start socketServer to send commands to robot


  
  
  
  
