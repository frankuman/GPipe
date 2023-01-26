import pip._vendor.requests as requests
import json
from requests.auth import HTTPBasicAuth
json_file_path = ""

android = "https://android-review.googlesource.com/"
opendev = "https://review.opendev.org/"
chromium = "https://chromium-review.googlesource.com/changes/"
def main():
    getOPEN = "/changes/"
    print("&&&")
    
    response = requests.get(chromium)
    print(response)
    text = response.text
    json.get(response)
    print(text)
    #json.load(respone)
    
if __name__ == "__main__":
    main()