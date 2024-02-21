import threading
import socket
import sys
import os

#=============#
port = 2233
#=============#

try :
    port = int( sys.argv[ 1 ] )
except :
    pass

os.chdir( os.path.split( __file__ )[ 0 ] )

def start( client : socket.socket , ip : tuple[ str , int ] ) :
    try :
        request = client.recv( 1024 ).decode().splitlines()
        client.send( "HTTP/1.1 200 OK\r\n\r\n".encode() )
        get = "." + request[ 0 ][ 4: ][ :-9 ]
        if get[ -1 ] == "/" :
            get += "index.html"
            print( f"{ ip[ 0 ] }:{ ip[ 1 ] }" )
        if not os.path.exists( get ) :
            get = "./404.html"
        with open( get , "rb" ) as file :
            client.send( file.read() )
        client.close()
    except :
        pass

tcp_socket = socket.socket( socket.AF_INET6 )
tcp_socket.setsockopt( socket.IPPROTO_IPV6 , socket.IPV6_V6ONLY , 0 )
tcp_socket.bind( ( "" , port ) )
tcp_socket.listen( 8 )

def server() :
    while 1 :
        client = threading.Thread( target = start , args = tcp_socket.accept() )
        client.start()
main = threading.Thread( target = server )
main.daemon = True
main.start()
print( f"http://127.0.0.1:{ port }" )

try :
    input()
except :
    pass
