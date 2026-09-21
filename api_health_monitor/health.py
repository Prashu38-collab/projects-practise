import requests


def check_api(url):
    try:
        response = requests.get(url, timeout=5)

        print("URL:", url)
        print("Status code:", response.status_code)

    except requests.exceptions.RequestException as error:
        print("Request failed:", error)


check_api("https://httpbin.org/status/200")
