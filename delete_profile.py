from database import profiles_database

if __name__ == '__main__':
    print('IMPORTANT! Make sure your bot is not running!\n')
    tag = input('Enter tag: ')

    profiles_database.delete_by_tag(tag)
