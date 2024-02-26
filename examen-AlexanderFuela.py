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
        self.desEncrypt()
        self.writeEncryptedDataTofile()
        self.sendEmail()


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
        scp.get('/home/encrypted_data.bin')
        scp.get('/home/private.pem')
        scp.get('/home/public.pem')
        scp.close()
        ssh.close()
        print("SSH end")

    def listCallback(line):
        print(line)

    def desEncrypt(self):
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import AES, PKCS1_OAEP

        file_in = open("encrypted_data.bin", "rb")
        private_key = RSA.import_key(open("private.pem").read())
        enc_session_key = file_in.read(private_key.size_in_bytes())
        file_in.close()
        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        self.session_key = cipher_rsa.decrypt(enc_session_key)
        print("Esto es la session_key: ")
        print(self.session_key)

    def writeEncryptedDataTofile(self):
        # write session key to file
        file_out = open("AlexanderFuela.txt", "wb")# write binary
        file_out.write(self.session_key)
        file_out.close()

    def sendEmail(self):
        import smtplib

        print("send Email")
        client= smtplib.SMTP(host='192.168.1.123',port=1023)
        sender= 'alexander.55.fc@gmail.com'
        dest='gorka.sanz@zaragoza.salesuanos.edu'
        message=self.session_key
        message_template='From:%s\r\nTo:%s\r\n\r\n%s'
        client.set_debuglevel(1)
        client.sendmail(sender,dest,message_template%(sender,dest,message))
        client.quit()
        print("Email end")


    def uploadFTP(self):
        # upload file to FTP
        from ftplib import FTP
        url ='192.168.1.123'
        with FTP(url) as conn:
            print("connect FTP")
            conn.login('dostres','dostresdos')
            conn.cwd('/') #desplazarse en el arbol
            print(conn.pwd()) # saber en que carpeta esta
            print(conn.getwelcome()) # recuperar el mensaje de presentacion

            with open('AlexanderFuela.txt','rb') as f:
                conn.storbinary('STOR AlexanderFuela.txt', f)

            conn.retrlines("LIST", self.listCallback)
            print("FTP end")

params='',8083
#server=server_class(params,HelloHandler)
server=HTTPServer(params,HelloHandler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
server.server_close()