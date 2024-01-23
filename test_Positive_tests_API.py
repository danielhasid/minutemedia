import uuid
from collections import Counter

import requests

ENDPOINT = "http://localhost:5000/users"
#check if Endpoint reached
def test_get_all_users():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_get_user_by_id():
    new_payload = generate_id()
    create_user_response = add_user(new_payload)#create new user
    assert create_user_response.status_code == 200
    get_user_response = get_user(new_payload['id']) #seraching the new user by passing the new ID
    assert get_user_response.status_code == 200
    get_user_data = get_user_response.json()
    assert get_user_data['id'] == new_payload['id']
    assert get_user_data['name'] == new_payload['name']



#create new user
def test_add_user():
    try:
        payload = generate_id()
        create_user_response = add_user(payload)
        assert create_user_response.status_code == 200    #Checking the status and the values returned
        data = create_user_response.json()
        assert payload['id'] == data['id']
        assert payload['name'] == data['name']
    except AssertionError:
        raise AssertionError("Failed to add user")
    #Verifing the new user is stored in DB with the correct values
    try:
        get_user_response = get_user(payload['id'])
        assert get_user_response.status_code == 200
        get_user_data = get_user_response.json()
        count_user = Counter(list(get_user_data)) #Check if the user added only once
        assert count_user['id'] == 1
        assert get_user_data['id'] == payload['id']
        assert get_user_data['name'] == payload['name']
    except:
        raise Exception("User NOT stored in DB")

#Edit User
def test_edit_user():
    payload = generate_id()
    create_user_response = add_user(payload)
    user_id = create_user_response.json()['id']

    user_data={"id":user_id,
             "name":"Reut",
            }
    update_user_response = edit_user(user_data,user_id)
    assert update_user_response.status_code == 200
    data = update_user_response.json()
    #verifing the returend Values
    assert data['id'] == user_id
    assert data['name'] == user_data['name']
    #checking if the data was saved
    get_user_response = get_user(user_id)
    assert get_user_response.status_code == 200
    edited_user = get_user_response.json()
    assert user_id == edited_user['id']
    assert user_data['name'] == edited_user['name']


def test_delete_user():
    payload = generate_id()
    create_user_response = add_user(payload)
    assert  create_user_response.status_code == 200
    data = create_user_response.json()
    user_id = data['id']
    #Delete the new user
    delete_user_response = delete_user(user_id)

    # if delete_user_response.status_code == 200:
    try:
        assert delete_user_response.status_code == 200
        returned_values = delete_user_response.json()
        #verify the returned list NOT contain the deleted user
        for value in returned_values:
            assert value['id'] != user_id
        get_user_response = get_user(user_id)
        assert get_user_response.status_code == 404
        assert get_user_response.text == 'user not found'
    except AssertionError:
        raise AssertionError(f"Failed to delete user No List returned: Status Code: {delete_user_response.status_code}.")



def add_user(payload):
    return requests.post(f"{ENDPOINT}",json=payload)

def get_user(user_id):
    return requests.get(f"{ENDPOINT}/{user_id}")

def edit_user(user_data,user_id):
    return requests.put(f"{ENDPOINT}/{user_id}", json=user_data)

def get_list_user(user_id):
    return requests.get(f"{ENDPOINT}/{user_id}")

def delete_user(user_id):
    return requests.delete(f"{ENDPOINT}/{user_id}")

def generate_id():
    user_id = f"test_user_{uuid.uuid4().hex}"
    return {
      "name": "Daniel",
      "id": user_id,
    }
