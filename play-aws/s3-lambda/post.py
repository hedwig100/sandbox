import requests

url = "https://httpbin.org/post"
files = {"file": open("README.md", "rb")}

r = requests.post(url, files=files)
print(r.text)
