from database import profiles_database

if __name__ == '__main__':
    print('IMPORTANT!\nTurn off the bot before removing profiles.\n')
    tag = input('Enter tag: ')

    profiles_database.delete_by_tag(tag)
