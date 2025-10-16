import requests
import os
import sys
import json


def main(args):
    url = "https://jsonplaceholder.typicode.com/todos/1"
    try:
        # make GET request
        response = requests.get(url)
        # check if request=success
        if response.status_code == 200:
            # parse json
            data = response.json()
            # print fetched JSON
            print("Fetched JSON data:")
            print(data)
            print(f"Title: {data['title']}")
            print(f"Completed: {data['id']}")
        else:
            print(f"Error: Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
if __name__ == "__main__":
    main(sys.argv[1:])