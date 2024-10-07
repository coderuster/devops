import urllib.request
import json

# Function to construct the URL for fetching raw content of a file from GitHub
def get_cmd(name, number):
    return f"https://raw.githubusercontent.com/coderuster/devops/main/{number}/{name}"

# Function to fetch the files from a specific folder in the repository
def get_files(repo_url, folder_path):
    api_url = f"{repo_url.rstrip('/')}/contents/{folder_path}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Required by GitHub's API
    req = urllib.request.Request(api_url, headers=headers)
    ret = []

    try:
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                contents = json.loads(response.read())
                # Collect only files
                files = [item["name"] for item in contents if item["type"] == "file"]
                ret = files
            else:
                print(f"Failed to fetch folder contents. Status code: {response.getcode()}")
    except Exception as e:
        print(f"Error fetching files: {e}")
    return ret

# Function to download and return the content of a file from GitHub
def https_get(url):
    headers = {"User-Agent": "Mozilla/5.0"}  # Required to avoid API errors
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                return response.read().decode()
            else:
                return f"Error: Unable to fetch content. Status code: {response.getcode()}"
    except Exception as e:
        return f"Error: {e}"

# Function to run the whole operation
def run_command(cmd):
    data = https_get(cmd)
    return data

def main():
    number = input("1\n2\n3\n4\n5\n6\n7\n8\n9\n10\nChoose: ").strip()
    repo_url = "https://api.github.com/repos/coderuster/devops"
    
    # Get the list of files from the selected folder
    files = get_files(repo_url, number)

    if not files:
        print("No files found or an error occurred.")
        return

    # Download each file and save it locally
    for f in files:
        cmd = get_cmd(f, number)
        print(f"Fetching content from {cmd}...")  # Feedback for the user
        content = run_command(cmd)

        # Save the content to a local file
        # Prevent auto-opening by just writing without any system call
        with open(f, "w", encoding="utf-8") as file:
            file.write(content)
            print(f"Saved {f} locally.")
    
if __name__ == "__main__":
    main()

