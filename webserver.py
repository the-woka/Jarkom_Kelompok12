from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes
import socket

class echoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Menentukan path jika path permintaan '/'
        if self.path == '/':
            self.path = '/index.html'
        # Menentukan path jika path permintaan '/pdf'
        elif self.path == '/pdf':
            self.path = '/TCPSocketProgramming.pdf'
        
        try:
            # Mendapatkan path ke direktori berdasarkan permintaan
            file_path = os.path.abspath(self.path[1:])
            if os.path.isfile(file_path):
                # Jika berkas ditemukan, membuka dan membaca file
                with open(file_path, 'rb') as file:
                    content = file.read()
                self.send_response(200)  # Mengirimkan respons dengan kode status 200 (OK)
                content_type, _ = mimetypes.guess_type(file_path)  # Menentukan tipe konten berdasarkan ekstensi berkas
                self.send_header('Content-type', content_type)  # Mengirimkan header tipe konten
            else:
                # Jika berkas tidak ditemukan, beralih ke FileNotFoundError
                raise FileNotFoundError
        except FileNotFoundError:
            # Jika berkas tidak ditemukan, mengirimkan respons dengan kode status 404 (File Not Found)
            content = b"<html><body><h1>404</h1><h3>File Not Found</h3></body></html>"
            self.send_response(404)
            self.send_header('Content-type', 'text/html')  # Mengirimkan header tipe konten

        self.send_header('Content-length', len(content))  # Mengirimkan header panjang konten
        self.end_headers()  # Mengakhiri header respons
        self.wfile.write(content)  # Menulis konten ke koneksi socket antara server dan klien

def main():
    HOST = 'localhost'
    PORT = 8000 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f'Server is running on {HOST}:{PORT}')
        while True:
            client_socket, client_address = server_socket.accept()  # Menerima koneksi dari klien
            handler = echoHandler(client_socket, client_address, server_socket)  # Menangani permintaan dari klien
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
