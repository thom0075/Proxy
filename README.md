# Proxy
A simple Python 3 proxy server

This proxy server is still under development. Certain features may not work correctly. Use it at your own risk.
Super-user privileges may be required for certain Operative systems such as GNU/Linux to use privileged ports such as 21, 80, 443 etc...
To run the server you must provide the necessary arguments:
  - Server IPv4 address as for example: 192.168.1.101
  - Server port (it must be an integer!)
  - Destination address or domain name as for example: example.domain.com
  - Destination port (again, ports numbers must be integers!)
  - "Receive first" flag to tell the server if it must receive something before establishing the connection (certain services such as FTP may send a welcome banner).
Some of this program's functionalities may be replaced with ScaPY's pre-built ones.
