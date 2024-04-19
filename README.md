# SocketsChatApp

## 1. Python Sockets usage

Now it is possible to run:
* As server module: 
  * socket_server_on_select.py
  * socket_server_on_selectors.py
  * socket_server_on_threading.py
* As client socket:
  * client_socket_on_threading.py

Current scripts work right.  
As for 'testing_scripts' package: I try to create async working socket app on generator functions.
Script works right, but server and client parts are in one module. Server could be run 
as simple python module from console, but clients should use 'nc' until in terminal to connect by host:port pair.


## 2. Syntax: 
1. **Broadcast** messages:  
   $ #broadcast::message_context
2. **Direct** messages:  
   $ #recipient_username::message_context
