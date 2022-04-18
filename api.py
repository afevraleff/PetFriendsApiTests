import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"
    def get_api_key(self, email, password):
        headers = {
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url+"api/key", headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
             result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {"auth_key": auth_key['key']}
        filter = {"filter": filter}
        res = requests.get(self.base_url + "api/pets", headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_api_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + "api/pets", headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_api_new_pet_simple(self, auth_key, name, animal_type, age):
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + "api/create_pet_simple", headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key, petId):
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + "api/pets/"+petId, headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_set_pet_photo(self, auth_key, petId, pet_photo):
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + "api/pets/set_photo/" + petId, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def put_change_pet_info(self, auth_key, petId, name, animal_type, age):
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.put(self.base_url + "api/pets/"+petId, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

