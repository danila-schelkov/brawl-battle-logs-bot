from database import profiles_database

if __name__ == '__main__':
    print('IMPORTANT! ВАЖНО!\nВыключи бота перед тем, как добавлять новый профиль.\n')
    tag = input('Введи тег: ')

    profiles_database.create_by_tag(tag)
