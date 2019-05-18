from modules.vk_auth import  VKAuth
from modules.friend import FriendSearch
from modules.db_file import DB_Mongo
from modules.user import User
from pprint import pprint
import json
import codecs


def get_potencial_friend_city_sex(friends, user_data):
    path_user_data = user_data['response'][0]
    friend_sex = input('Введите пол для поиска друзей. 0 - все, 1 - Ж, 2 - М. : ')
    if 'city' not in user_data['response'][0]:
        path_user_data['city'] = {'id': 0, 'title': ''}
        path_user_data['city']['id'] = input('Введите порядковый номер города (В Контакте)по,'
                                             ' которому нужно проводить поиск: ')
    if 'bdate' not in user_data['response'][0]:
        path_user_data['bdate'] = ''
        path_user_data['bdate'] = input('Введите дату рождения в формате "D.M.YYYY": ')
    if len(user_data['response'][0]['bdate']) < 6:
        path_user_data['bdate'] = ''
        path_user_data['bdate'] = input('Введите дату рождения в формате "D.M.YYYY": ')
    potencial_friend_city_sex_out = friends.get_partners_by_basic(friend_sex, path_user_data['city']['id'])['response']
    return potencial_friend_city_sex_out


def db_operation(db_in, partners_basic_in, user_data, friends, user_id):
    for item in partners_basic_in['list_friend']:
        db_in.import_data(item)
    print('Формируем список потенциальных друзей для {}'.format((user_data['response'][0]['first_name']))
          + ' ' + (user_data['response'][0]['last_name']))
    db_in.put_fields()  # создаем дополнительные поля
    basic_id = db_in.get_basic_id()
    print('Получили список {} потенциальных друзей'.format(len(basic_id)))
    max = input('Введите насколько лет друг может быть старше: ')
    min = input('Введите насколько лет друг может быть младше: ')
    db_in.put_value_bdate(user_data['response'][0]['bdate'], max, min)  # отметили в БД людей по возрасту
    record_number = 0
    for id in basic_id:
        print('Поиск общих друзей и общих групп потенциального друга №: {}'.format(record_number + 1))
        if friends.get_com_friends(user_id, id) > 1:  # отметили в БД людей с общими друзьями
             db_in.put_value_com(id)
        if friends.get_com_groups(user_id, id) > 1:  # отметили в БД людей с общими группами
            db_in.put_value_com_2(id)
        record_number += 1
    if 'interests' in user_data['response'][0].keys():
        for part in user_data['response'][0]['interests'].split():  # отметили людей по общим интересам
            db_in.put_value_inter(part)


def sort_potencial_friend():
    crit_dict = {'com_friends': 0, 'com_bdate': 0, 'com_groups': 0, 'com_interests': 0}
    crit_dict['com_friends'] = input('Введите вес для критерия - Общие друзья (от 1 до 4): ')
    crit_dict['com_bdate'] = input('Введите вес для критерия - Возраст (от 1 до 4): ')
    crit_dict['com_groups'] = input('Введите вес для критерия - Общие группы (от 1 до 4): ')
    crit_dict['com_interests'] = input('Введите вес для критерия - Интересы (от 1 до 4): ')
    return crit_dict


def list_to_json(out_list, path_f):
    with codecs.open(path_f, 'w', encoding='utf-8') as json_file:
        json.dump(out_list, json_file, ensure_ascii=False)


def main():
    get_auth = VKAuth(['friends'], '6892678', '5.95')
    get_auth.auth()
    print('Получен следующий токен {}'.format(get_auth._access_token))  # получили токен пользователя
    user_input = input('Введите id или имя пользователя: ')
    user = User(get_auth._access_token)
    user_id = user.check_user(user_input)
    user_data = user.get_user_data(user_id)
    friends = FriendSearch(get_auth._access_token, user_id)
    db = DB_Mongo()
    db.all_drop()
    potencial_friend_city_sex = get_potencial_friend_city_sex(friends, user_data)  # Получаем список из VK
    db_operation(db, potencial_friend_city_sex, user_data, friends, user_id)  # запись базовый список в БД
    selection_criterion = sort_potencial_friend()  # формируем уточняющие критерии
    out_db = db.find_n_drop_adv(selection_criterion)  # сортируем по уточняющим критериям
    out_list = []
    for item in out_db.find():
        x = friends.get_fr(item['id'])
        out_list.append(x)
    list_to_json(out_list, 'outjson.json')
    pprint(out_list)


if __name__ == "__main__":
    main()
