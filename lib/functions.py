import requests

def download_image(url, file_name):
    def download_image(url, file_name):
    headers = {
        "User-Agent": "Chrome/51.0.2704.103",
    }
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
    else:
        return 1

def download_image_into_memory(url):
    headers = {
        "User-Agent": "Chrome/51.0.2704.103",
    }
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        byte_stream = BytesIO(response.content)
        byte_array = byte_stream.getvalue()
        return byte_array
    else:
        return 1
