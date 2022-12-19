from database import profiles_database

if __name__ == '__main__':
    print('IMPORTANT!\nTurn off the bot before adding new profiles.\n')
    tag = input('Enter tag: ')

    profiles_database.create_by_tag(tag)
