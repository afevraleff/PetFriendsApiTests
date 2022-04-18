from api import PetFriends
from settings import valid_email, valid_password


pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_api_new_pet(auth_key, "Murka", 'dich', '12', 'images/cat.jpg')
    assert status == 200

def test_add_new_pet_simple_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_api_new_pet_simple(auth_key, "Chebur", 'food', '12')
    assert status == 200

def test_delete_pet_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.delete_pet(auth_key, my_pets['pets'][-1]['id'])
        assert status == 200
    else:
        raise Exception("There is no my pets")

def test_set_pet_photo_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.post_set_pet_photo(auth_key, my_pets['pets'][-1]['id'], "images/dog.jpg")
        assert status == 200
        assert result['name'] == my_pets['pets'][-1]["name"]
    else:
        raise Exception("There is no my pets")

def test_successful_update_self_pet_info(name='Мурзик',
                                         animal_type='Котэ', age='5'):
   _, auth_key = pf.get_api_key(valid_email, valid_password)
   _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

   if len(my_pets['pets']) > 0:
       status, result = pf.put_change_pet_info(auth_key, my_pets['pets'][0]['id'],
                                                name, animal_type, age)
       assert status == 200
       assert result['name'] == name
   else:
       raise Exception("There is no my pets")

#Негативные тесты

def test_get_api_key_for_valid_user_invalid_password(email=valid_email, password="123"):
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert "This user wasn't found in database" in result
    assert "key" not in result

def test_get_api_key_for_invalid_user(email="mail@mail.ru", password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert "key" not in result
    assert "This user wasn't found in database" in result

def test_get_all_pets_with_invalid_key(filter='', auth_key={"key": '123'}):
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200
    assert "Please provide 'auth_key' Header" in result

def test_delete_pet_with_invalid_key_valid_pet_id(auth_key={"key":"123"}):
    status, result = pf.delete_pet(auth_key, "a823ca47-9413-4157-aee3-616c6b6f6d3b")
    assert status != 200
    assert "Please provide 'auth_key' Header" in result

def test_delete_pet_with_valid_key_invalid_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.delete_pet(auth_key, "fghfds123")
        assert status != 200
        print(result)
    else:
        raise Exception("There is no my pets")
# В тесте на вход подается неверный pet_id, статус ответа 200. Возможно это баг. Так как питомец при этом не удаляется

def test_add_new_pet_simple_with_invalid_key(auth_key={"key": "123"}):
    status, result = pf.post_api_new_pet_simple(auth_key, "Cheb", 'food', '12')
    assert status != 200
    assert "Please provide 'auth_key' Header" in result

def test_add_new_pet_with_invalid_key(auth_key={"key": "123"}):
    status, result = pf.post_api_new_pet(auth_key, "Murka2", 'dich', '12', 'images/cat.jpg')
    assert status != 200
    assert "Please provide 'auth_key' Header" in result

def test_set_pet_photo_with_invalid_key_valid_pet_id(auth_key={"key": "123"}, petId="a823ca47-9413-4157-aee3-616c6b6f6d3b"):
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.post_set_pet_photo(auth_key, petId, "images/dog.jpg")
    assert status != 200
    assert "Please provide 'auth_key' Header" in result

def test_successful_update_self_pet_info_valid_key_invalid_pet_id(name='Мурз',
                                         animal_type='Кошка', age='5'):
   _, auth_key = pf.get_api_key(valid_email, valid_password)
   _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

   if len(my_pets['pets']) > 0:
       status, result = pf.put_change_pet_info(auth_key, "1fefr24",
                                                name, animal_type, age)
       assert status != 200
       assert "Pet with this id wasn't found!" in result
   else:
       raise Exception("There is no my pets")

def test_successful_update_self_pet_info_invalid_key_valid_petId(auth_key={"key": "123"}, name='Мурз',
                                         animal_type='Кошка', age='5'):
    status, result = pf.put_change_pet_info(auth_key, "a823ca47-9413-4157-aee3-616c6b6f6d3b",
                                                name, animal_type, age)
    assert status != 200
    assert "Please provide 'auth_key' Header" in result