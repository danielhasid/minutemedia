import itertools
import uuid

import pytest
import requests


ENDPOINT = "http://localhost:5000/users"


def test_get_user_details():
    payload_option = get_invalid_values()
    for item in payload_option:
        user_id = item[0]
        get_user_response = get_user(user_id)
        assert get_user_response.status_code == 404

def test_add_user_exists_id():
    payload = user_payload()
    create_user_response = add_user(payload)
    assert create_user_response.status_code == 200
    exists_id = payload['id']
    exists_user_response = get_users()
    assert exists_user_response.status_code == 200
    user_data = {
        "name": "Exists User",
        "id": exists_id,
    }
    create_user_response = add_user(user_data)
    if create_user_response.status_code == 200:
        raise Exception(f"User added with exists ID,{payload['id']}")
    else:
        assert create_user_response.status_code == 404

def test_add_user():
    payload_option = get_invalid_values()
    for item in payload_option:
        payload= {
          "name": item[0],
          "id": item[1],
        }
        create_user_response = add_user(payload)
        if create_user_response.status_code == 200:
            raise Exception(f"User added with Invalid values {payload['name']},{payload['id']}")
        else:
            assert create_user_response.status_code == 404


def test_edit_id_user():
    payload = user_payload()
    create_user_response = add_user(payload)
    user_id = create_user_response.json()['id']
    exists_user_response = get_users()
    exists_id = exists_user_response.json()
    user_data = {
        "name": "Test",
        "id": exists_id[0]['id'],
    }

    update_user_response = update_user(user_data,user_id)
    if update_user_response.status_code == 200:
        raise Exception(f"ERROR ... ID field have been updated with exists ID {user_data['id']}")
    else:
        assert update_user_response.status_code == 404


def test_edit_user():
    payload = user_payload()
    create_user_response = add_user(payload)
    user_id = create_user_response.json()['id']
    payload_option = get_invalid_values()
    for item in payload_option:
        payload = {
            "name": user_id,
            "id": item[1],
        }
    update_user_response = update_user(payload,user_id)
    if update_user_response.status_code == 200:
        raise Exception(f"ERROR ... Name field has been updated with invalid values")
    else:
        assert update_user_response.status_code == 404

#delete user using invalid ID data type
def test_delete_user():
    payload_option = get_invalid_values()
    for item in payload_option:
        user_id = item[0]
        delete_user_response = delete_user(user_id)
        if delete_user_response.status_code == 200:
            raise Exception(f"API accept all types of values in id field ONLY string should allowed")
        if isinstance(item[0],str): #chckes the response code ID data type
            assert delete_user_response.status_code == 404
        else:
            assert delete_user_response.status_code == 500

def add_user(payload):
    return requests.post(f"{ENDPOINT}",json=payload)

def get_user(user_id):
    return requests.get(f"{ENDPOINT}/{user_id}")

def get_users():
    return requests.get(f"{ENDPOINT}")

def update_user(user_data,user_id):
    return requests.put(f"{ENDPOINT}/{user_id}", json=user_data)

def get_list_user(user_id):
    return requests.get(f"{ENDPOINT}/{user_id}")

def delete_user(user_id):
    return requests.delete(f"{ENDPOINT}/{user_id}")



def get_invalid_values():
    options = ["", None,True,False,235313]
    matrix = [list(pair) for pair in itertools.product(options, repeat=2)]

    for item in matrix:
        yield item

def user_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    return {
      "name": "Daniel",
      "id": user_id,
    }
