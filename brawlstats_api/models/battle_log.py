from datetime import datetime

from brawlstats_api.models.battle import Battle
from utilities import add_spaces


class BattleLog:
    def __init__(self):
        self.start_timestamp: int = -1
        self.battle: Battle or None = None
        self.event: dict or None = None

    def get_battle_description(self,
                               own_player: dict,
                               own_team: list) -> tuple[str, int]:
        description = f'Player found in match!\n'

        player_name = own_player['name']
        brawler_name = own_player['brawler']['name']
        description += f'**{player_name}** played **{brawler_name}**'
        if 'trophies' in own_player['brawler']:
            brawler_trophies = own_player['brawler']['trophies']
            description += f' at **{brawler_trophies}** trophies'

        description += '\n\n'

        description += f'Match info: \n'

        game_mode = self.event['mode']
        description += f'Mode: **{add_spaces(game_mode)}**\n'

        map_name = self.event['map']
        description += f'Map: **{map_name}**\n'

        description += '\n'

        if own_team is not None:
            description += f'Team:\n'
            for player in own_team:
                teammate_player_name = player['name']
                teammate_brawler_name = player['brawler']['name'].capitalize()

                teammate_brawler_trophies = None
                if 'trophies' in player['brawler']:
                    teammate_brawler_trophies = player['brawler']['trophies']

                description += f'**{teammate_brawler_name}** ({teammate_player_name}) '
                if teammate_brawler_trophies is not None:
                    description += f' at **{teammate_brawler_trophies}** trophies'
                description += '\n'

            description += '\n'

        description += f'Match results: \n'

        minutes_ago = int((datetime.utcnow().timestamp() - self.start_timestamp) / 60)
        description += f'Time: **{minutes_ago} minutes ago**\n'
        description += f'Result: **{self.battle.get_result_text().upper()}**'

        trophy_change = 0
        if self.battle.trophy_change is not None:
            trophy_change = self.battle.trophy_change
            description += f' ({trophy_change} trophies)'

        return description, trophy_change

    @classmethod
    def wrap(cls, battle_log_data: dict):
        battle_log = cls()
        battle_log.start_timestamp = int(datetime.strptime(
            battle_log_data['battleTime'],
            '%Y%m%dT%H%M%S.000Z'
        ).timestamp())

        battle_log.event = battle_log_data['event']
        battle_log.battle = Battle.wrap(battle_log_data['battle'])

        return battle_log
