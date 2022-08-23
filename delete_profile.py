from database import profiles_database

if __name__ == '__main__':
    print('IMPORTANT! ВАЖНО!\nВыключи бота перед тем, как удалять профиль.\n')
    tag = input('Введи тег: ')

    profiles_database.delete_by_tag(tag)
