from database.profiles import Profiles

print('IMPORTANT! ВАЖНО!\nВыключи бота перед тем, как добавлять новый профиль.\n')
tag = input('Введи тег: ').strip()

profiles = Profiles()
profiles.delete_by_tag(tag)
