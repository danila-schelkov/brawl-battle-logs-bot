from datetime import datetime

from database import Database
from models.profile import Profile


class Profiles(Database):
    def __init__(self):
        super().__init__(f'./{"database/" if __name__ != "__main__" else ""}profiles.db')

        self.execute("""CREATE TABLE IF NOT EXISTS profiles (
            `id` INTEGER PRIMARY KEY NOT NULL, 
            `last_battle_timestamp` INTEGER NOT NULL
        )""")

        self.cached_profiles = {

        }

    def create_by_tag(self, tag: str) -> Profile:
        profile = Profile()
        profile.tag = tag

        return self.create(profile.id)

    def create(self, profile_id: int) -> Profile:
        exists = self.exists('profiles', 'id', profile_id)

        if not exists:
            self.execute(f'INSERT into profiles (id, last_battle_timestamp) values '
                         f'({profile_id}, {datetime.utcnow().timestamp()})')

            self.commit()

        return self.get(profile_id)

    def get(self, profile_id: int) -> Profile or None:
        if not (profile_id in self.cached_profiles):
            exists = self.exists('profiles', 'id', profile_id)

            if exists:
                profile_data = self.select('profiles', None, ('id', profile_id), 1)[0]

                profile = Profile()
                profile.load(profile_data)
                self.cached_profiles[profile_id] = profile
            else:
                return None

        return self.cached_profiles[profile_id]

    def update(self, profile: Profile, **kwargs):
        super().update('profiles', [
            ('last_battle_timestamp', profile.last_battle_timestamp)
        ], ('id', profile.id))

        self.commit()

    def get_all(self):
        profile_ids = self.select('profiles', 'id')
        if isinstance(profile_ids, int):
            profile_ids = [profile_ids]

        return [self.get(profile_id) for profile_id in profile_ids]
