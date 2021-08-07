from database.profiles import Profiles

print('IMPORTANT! ВАЖНО!\nВыключи бота перед тем, как добавлять новый профиль.\n')
tag = input('Введи тег: ').strip()

profiles = Profiles()
profiles.create_by_tag(tag)
