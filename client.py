import socket
import sys
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 1027)
print >>sys.stderr, 'Client: connecting to %s port %s' % server_address
sock.connect(server_address)
try:# Send data
    message = 'new-account:erfan:1234\\n'
    print ( 'Client: sending "{}"'.format(message))
    sock.sendall(message)
    #for i in range(1000):
    #    print()
    message = 'new-dir:/:perfan\\n'
    print( 'Client: sending "{}"'.format(message))
    sock.sendall(message)
    #for i in range(1000):
    #    print()
    message = 'ren-dir:/:mvd:ali\\n'
    print( 'Client: sending "{}"'.format(message))
    #sock.sendall(message)
    #for i in range(1000):
    #    print()
    message = 'unshare-dir:/:fuckerfan:ali\\n'
    print( 'Client: sending "{}"'.format(message))
    #sock.sendall(message)    
    
    #for i in range(1000):
    #    print()
    message = 'logout\\n'
    print( 'Client: sending "{}"'.format(message))
    sock.sendall(message)
    # Look for the response
#    amount_received = 0
#    amount_expected = 1

#    while amount_received < amount_expected:
#        data = sock.recv(4096)
#        amount_received += len(data)
#        print >>sys.stderr, 'Client: received "%s"' % data
    
finally:
    print >>sys.stderr, 'Client: closing socket'
    sock.close()
