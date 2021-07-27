## create a little habit tracking app, with the help of pixe.la


import requests
from datetime import datetime

PIXELA_API = "https://pixe.la/v1/users"
TOKEN = "YOUR TOKEN"
USERNAME = "YOUR USERNAME"
GRAPH_ID = "YOUR GRAPH NAME"
user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# create an acoung - only once
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

# create a graph
graph_endpoint = f"{PIXELA_API}/{USERNAME}/graphs"
graph_params = {
    "id": GRAPH_ID,
    "name": "Coding",
    "unit": "minutes",
    "type": "float",
    "color": "ajisai",
}

headers = {
    "X-USER-TOKEN": TOKEN,
}

# response = requests.post(url=graph_endpoint, json=graph_params, headers=headers)
# print(response.text)

# add an entry for today
pixel_creation_endpoint = f"{PIXELA_API}/{USERNAME}/graphs/{GRAPH_ID}"

today = datetime.now()
pixel_data = {
    "date": today.strftime("%Y%m%d"),
    "quantity": input("How many minutes did you code today? "),
}

response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
print(response.text)


update_endpoint = f"{PIXELA_API}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

new_pixel_data = {
    "quantity": "20.5"
}


#  option to change the input
## PUT
# response = requests.put(url=update_endpoint, json=new_pixel_data, headers=headers)
# print(response.text)


## option to delete certain points
delete = f"{PIXELA_API}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

## DELETE
# response = requests.delete(url=delete, headers=headers)
# print(response.text)