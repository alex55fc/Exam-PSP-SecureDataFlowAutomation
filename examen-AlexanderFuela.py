#!/usr/bin/python3
#!pip3 install scp

from http.server import BaseHTTPRequestHandler,HTTPServer

class   HelloHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
    def do_GET(self):
        self.do_HEAD()
        self.wfile.write("""<html><head><title>Hello
            World</title></head><body><p>HelloWorld</p>
            <form method="POST" >
            <input type="submit" value="Click me" />
            </form>
            </body></html>""".encode("utf-8"))
    def do_POST(self):
        self.do_HEAD()
        self.passTheExam()
        
        
    def passTheExam(self):
        self.connectSSH()


#para probar el servidor
#ssh -p 2222 linuxserver@127.0.0.1
    def connectSSH(self):
        from scp import SCPClient
        import paramiko
        print("connect SSH")
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname='192.168.1.123', port='2222',username='tresdos', password='tresdos')
        print("SSH connected")

        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport())
        scp.get('public.pem')
        scp.get('encrypted.bin')
        scp.get('private.pem')
        scp.close()
        ssh.close()
        print("SSH end")

    def listCallback(line):
        print(line)

params='',8083
#server=server_class(params,HelloHandler)
server=HTTPServer(params,HelloHandler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
server.server_close()