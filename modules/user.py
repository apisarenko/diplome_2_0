import requests
import time


class UserVK:
    def __init__(self, token):
        self.token = token


class User(UserVK):
    def __init__(self, token):
        super().__init__(token)

    def check_user(self, user_input):

        try:
            int(user_input)
            try:
                params = {
                    'access_token': self.token,
                    'user_ids': self.user_input,
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


class FriendSearch(UserVK):
    def __init__(self, token, id):
        super().__init__(token)
        self.id = id

    def vk_request(self, params_in):
        response = requests.get(
            'https://api.vk.com/method/execute',
            params_in
        )
        time.sleep(0.33)
        out = response.json()
        return response.json()

    def check_resp(self, resp_in):
        if resp_in['response']['fr_friends'] != None:
            if resp_in['response']['usr_friends'] != None:
                return len(list(set(resp_in['response']['usr_friends']) & set(resp_in['response']['fr_friends'])))
            else:
                return 0
        else:
            return 0

    def check_resp_2(self, resp_in):
        if resp_in['response']['fr_groups'] != None:
            if resp_in['response']['usr_groups'] != None:
                return len(list(set(resp_in['response']['usr_groups']) & set(resp_in['response']['fr_groups'])))
            else:
                return 0
        else:
            return 0

    def get_partners_by_basic(self, sex_friend, city_friend):
        params = {'access_token': self.token, 'v': 5.95,
                  'code': ''
                  'var sex_friend = ' + str(sex_friend) + ';'

                  'var list_friend = API.users.search({count: 250, '
                  'city:' + str(city_friend) + ', status: 6,'
                  'sex: sex_friend});'

                  'var params_friend = API.users.get({user_ids: list_friend.items@.id, '
                  'fields: "sex, bdate, city, interests, relation"});'

                  'return {"list_friend":params_friend};'
                  }
        try:
            return self.vk_request(params)
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения. Ждем 5 сек после чего попытается восстановить связь!')
            time.sleep(5)
            try:
                return self.vk_request(params)
            except requests.exceptions.ConnectionError:
                print('Ошибка соединения. Ждем 10 сек после чего попытается восстановить связь!')
                time.sleep(10)
                try:
                    return self.vk_request(params)
                except requests.exceptions.ConnectionError:
                    print('Ошибка соединения. Завершение работы Программы.')

    def get_com_friends(self, usr_id, fr_id):
        params = {'access_token': self.token, 'v': 5.95,
                  'code': ''
                  'var usr_friends = API.friends.get({user_id:' + str(usr_id) + '}).items;'  # друзья User
                  'var fr_friends = API.friends.get({user_id:' + str(fr_id) + '}).items;'  # друзья друга
                  'return {"usr_friends":usr_friends, "fr_friends":fr_friends};'
                  }
        try:
            req = self.vk_request(params)
            return self.check_resp(req)
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения. Ждем 5 сек после чего попытается восстановить связь!')
            time.sleep(5)
            try:
                req = self.vk_request(params)
                return self.check_resp(req)
            except requests.exceptions.ConnectionError:
                print('Ошибка соединения. Ждем 10 сек после чего попытается восстановить связь!')
                time.sleep(10)
                try:
                    req = self.vk_request(params)
                    return self.check_resp(req)
                except requests.exceptions.ConnectionError:
                    print('Ошибка соединения. Завершение работы Программы.')

    def get_com_groups(self, usr_id, fr_id):
        params = {'access_token': self.token, 'v': 5.95,
                  'code': ''
                  'var usr_groups =API.groups.get({user_id:' + str(usr_id) + '}).items;'  # группы User
                  'var fr_groups =API.groups.get({user_id:' + str(fr_id) + '}).items;'  # группы друга
                  'return {"usr_groups":usr_groups, "fr_groups":fr_groups};'
                  }
        try:
            req = self.vk_request(params)
            return self.check_resp_2(req)
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения. Ждем 5 сек после чего попытается восстановить связь!')
            time.sleep(5)
            try:
                req = self.vk_request(params)
                return self.check_resp(req)
            except requests.exceptions.ConnectionError:
                print('Ошибка соединения. Ждем 10 сек после чего попытается восстановить связь!')
                time.sleep(10)
                try:
                    req = self.vk_request(params)
                    return self.check_resp(req)
                except requests.exceptions.ConnectionError:
                    print('Ошибка соединения. Завершение работы Программы.')

    def get_fr(self, id):
        params = {
            'owner_id': id,
            'access_token': self.token,
            'v': 5.95,
            'extended': '1',
            'album_id': 'profile'
        }
        try:
            response_fr_json = requests.get(
                'https://api.vk.com/method/photos.get',
                params
            )
        except Exception as e:
            print(response_fr_json.json()['error']['error_msg'])

        if 'error' not in response_fr_json.json():
            url_photos = []
            flag = 0
            photos = response_fr_json.json()['response']['items']
            photos = sorted(photos, key=lambda k: k['likes']['count'])  # сортировка фото по лайкам
            photos = photos[-3:]
            for item in photos:
                flag = 0
                for size in item['sizes']:
                    if size['type'] == 'o':  # ссылку на фото в оригинальном качестве
                        url_photos.append(size['url'])
                        flag = 1
                if flag == 0:  # если такое ориг. кач-во нет то загружаем качество первое в списке
                    url_photos.append(item['sizes'][0]['url'])
            fr_out = {'usr_url': 'https://vk.com/id' + str(photos[0]['owner_id']), 'top3_photos': url_photos}
        else:
            fr_out = {'usr_url': 'https://vk.com/id' + str(id), 'top3_photos': 'private profile'}
        return fr_out
