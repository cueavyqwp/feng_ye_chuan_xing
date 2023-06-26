import threading
import socket
import sys
import os

#=============#
port = 2233
#=============#

try :
    port = int( sys.argv[1] )
except :
    pass

os.chdir( os.path.split( __file__ )[0] ) # 

def start( client : socket.socket , ip : tuple ) :
    request = client.recv( 1024 ).decode().splitlines()
    client.send("HTTP/1.1 200 OK\r\n\r\n".encode())
    get = "." + request[ 0 ][ 4: ][ :-9 ]
    if get[ -1 ] == "/" :
        get += "index.html"
        print( f"{ ip[0] }:{ ip[1] }" )
    if os.path.exists( get ) :
        with open( get , "rb" ) as file :
            client.send( file.read() )
    client.close()

tcp_socket = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
tcp_socket.bind( ( "" , port ) )
tcp_socket.listen( 8 )
print( f"http://127.0.0.1:{ port }" )

while 1 :
    client = threading.Thread( target= start , args = tcp_socket.accept() )
    client.start()
