import socket
import ssl
import urllib.request
import json

def get_cmd(name,number):
    return f"raw.githubusercontent.com/coderuster/fds/main/{number}/{name}"


def get_files(repo_url, folder_path):
    api_url = f"{repo_url.rstrip('/')}/contents/{folder_path}"
    ret=[]
    with urllib.request.urlopen(api_url) as response:
        if response.getcode() == 200:
            contents = json.loads(response.read())
            
            for item in contents:
                if item["type"] == "file":
                    filename = item["name"]
                    ret.append(filename)
        else:
            print(f"Failed to fetch folder contents. Status code: {response.getcode()}")
    return ret
def https_get(url):
    hostname, _, path = url.partition('/')
    if not path:
        path = '/'
    with socket.create_connection((hostname, 443)) as sock:
        context = ssl.create_default_context()
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
            ssock.sendall(request.encode())

            response = b""
            while True:
                data = ssock.recv(4096)
                if not data:
                    break
                response += data
    body_start = response.find(b"\r\n\r\n") + len(b"\r\n\r\n")
    return response[body_start:].decode()

def run_command(cmd):
  try:
      data=https_get(cmd)
      return data
  except Exception as e:
    print(f"Error: {e}")
    return "ERROR"

def main():
    number=input("1[arithmetic operation]\n2[1D array]\n3[2D array]\n4[alice,bob]\n5[pandas]\n6[text processing]\n7[2D array]\nChoose: ").strip()
    repo_url = "https://api.github.com/repos/coderuster/fds/"
    files=get_files(repo_url,number)
    # files=["server.py","client.py"]
    for f in files:
        cmd=get_cmd(f,number)
        content=run_command(cmd)
        with open(f,"w") as file:
            file.write(content)
if __name__=="__main__":
    main()
