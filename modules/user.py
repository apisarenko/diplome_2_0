import requests


class User:
    def __init__(self, token):
        self.token = token

    def check_user(self, user_input):
        try:
            int(user_input)
            try:
                params = {
                    'access_token': self.token,
                    'user_ids': user_input,
                    'v': 5.95,
                    'fields': 'sex, bdate, city, interests, relation'
                }
                response_get_id = requests.get(
                    'https://api.vk.com/method/users.get',
                    params
                )
                user_input = int(response_get_id.json()['response'][0]['id'])
            except KeyError:
                print('Пользователя с таким id не существует!')
                exit(0)
        except ValueError:
            try:
                params = {
                    'access_token': self.token,
                    'user_ids': user_input,
                    'v': 5.95,
                    'fields': 'sex, bdate, city, interests, relation'
                }
                response_get_id = requests.get(
                    'https://api.vk.com/method/users.get',
                    params
                )
                user_input = int(response_get_id.json()['response'][0]['id'])
            except KeyError:
                print('Пользователя с таким именем не существует!')
                exit(0)
        return user_input

    def get_user_data(self, user_id):
        params = {
            'access_token': self.token,
            'user_ids': user_id,
            'v': 5.95,
            'fields': 'sex, bdate, city, interests, relation'
        }
        try:
            response_get_user_data = requests.get(
                'https://api.vk.com/method/users.get',
                params
            )
            return response_get_user_data.json()
        except Exception as e:
            print(response_get_user_data.json()['error']['error_msg'])
