from api import PetFriends
from settings import val_email, val_password, inval_email, inval_password
import os

pf = PetFriends()

# проверка статуса 200 + и переменная result содержит key
def test_get_api_key_for_valid_user(email=val_email, password=val_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

# проверка статуса 200 + список питомцев не пустой
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

# проверка добавления питомца с валидными данными + проверка статуса 200
def test_add_new_pet_with_valid_data(name='Тихан-Тиханыч', animal_type='котик', age='7', pet_photo='images/1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# проверка возможности удаления питомца
def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(val_email, val_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Тест1", "Тест2", "8", "images/3.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

# проверка возможности изменить данные питомца
def test_update_pet_info(name='Курочка', animal_type='котик', age='1'):
    _, api_key = pf.get_api_key(val_email, val_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")

# проверка запроса с невалидным паролем на получение ключа
def test_get_api_key_invalid_password(email=val_email, password=inval_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# проверка запроса с невалидным емайлом на получение ключа
def test_get_api_key_invalid_email(email=inval_email, password=val_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# проверка добавления питомца без фото
def test_add_pet_without_a_photo(name='Cat', animal_type='cat', age='32'):
    _, api_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet_set_photo(api_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# добавить/обновить фото последнему созданному питомцу
def test_add_photo_at_pet(pet_photo='images/2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(val_email, val_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Питомцы отсутствуют")

# проверка добавления питомца с пустым значением, например, animal type
def test_add_pet_with_empty_value(name='Тишаня', animal_type='', age='7', pet_photo='images/1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['animal_type'] != ''

# проверка добавления питомца с отрицательным значением в возрасте
def test_add_pet_negative_value(name='Тихан-Тиханыч', animal_type='котик', age='-7', pet_photo='images/1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert age not in result['age']

# проверка добавления питомца с цифрами в переменных, например, animal_type
def test_add_pet_variable_animal_type_number(name='tihan', animal_type='76876', age='3', pet_photo='images/2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert animal_type not in result['animal_type']

# проверка добавления питомца с цифрами в переменных, например, name
def test_add_pet_variable_name_number(name='4238', animal_type='76876', age='4', pet_photo='images/2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert animal_type not in result['animal_type'], 'Питомец добавлен на сайт с цифрами вместо букв в поле порода'

# проверка добавления питомца c возрастом не больше двухзначного числа
def test_add_pet_variable_age(name='Степашка', animal_type='cat', age='121', pet_photo='images/3.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(val_email, val_password)
    _, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    number = result['age']
    assert len(number) != 2