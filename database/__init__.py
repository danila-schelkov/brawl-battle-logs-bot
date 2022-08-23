import atexit

from database.profiles_database import ProfilesDatabase

profiles_database = ProfilesDatabase()


def close_all_databases():
    profiles_database.close()


atexit.register(close_all_databases)
