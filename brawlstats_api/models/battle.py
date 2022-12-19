from models import Profile


class Battle:
    def __init__(self):
        self.type: str or None = None
        self.trophy_change: int or None = None

        self._teams: list = []
        self._players: list = []
        self._rank: int or None = None
        self._result: str or None = None

    def get_player_and_team(self, profile: Profile) -> tuple[dict or None, list or None]:
        """Finds player and team by profile tag.

        :param profile: profile to find
        :return:
        """

        for team in self._teams:
            for player in team:
                if player['tag'][1:] == profile.get_tag():
                    return player, team

        for player in self._players:
            if player['tag'][1:] == profile.get_tag():
                return player, None

        return None, None

    def get_result_text(self):
        if self._rank is not None:
            return str(self._rank) + ' place'

        return self._result

    @classmethod
    def wrap(cls, battle_data):
        battle = cls()

        if 'type' in battle_data:
            battle.type = battle_data['type']

        if 'trophyChange' in battle_data:
            battle.trophy_change = battle_data['trophyChange']

        if 'teams' in battle_data:
            battle._teams = battle_data['teams']
        if 'players' in battle_data:
            battle._players = battle_data['players']

        if 'rank' in battle_data:
            battle._rank = battle_data['rank']
        else:
            battle._result = battle_data['result']

        return battle
