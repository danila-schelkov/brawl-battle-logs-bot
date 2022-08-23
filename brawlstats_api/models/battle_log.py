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
        description = f'Игрок замечен в игре!\n'

        player_name = own_player['name']
        brawler_name = own_player['brawler']['name']
        description += f'**{player_name}** играл на **{brawler_name}**'
        if 'trophies' in own_player['brawler']:
            brawler_trophies = own_player['brawler']['trophies']
            description += f' на **{brawler_trophies}** кубках'

        description += '\n\n'

        description += f'Информация матча: \n'

        game_mode = self.event['mode']
        description += f'Режим: **{add_spaces(game_mode)}**\n'

        map_name = self.event['map']
        description += f'Карта: **{map_name}**\n'

        description += '\n'

        if own_team is not None:
            description += f'Команда:\n'
            for player in own_team:
                teammate_player_name = player['name']
                teammate_brawler_name = player['brawler']['name'].capitalize()

                teammate_brawler_trophies = None
                if 'trophies' in player['brawler']:
                    teammate_brawler_trophies = player['brawler']['trophies']

                description += f'**{teammate_brawler_name}** ({teammate_player_name}) '
                if teammate_brawler_trophies is not None:
                    description += f' на **{teammate_brawler_trophies}** кубков'
                description += '\n'

            description += '\n'

        description += f'Результаты матча: \n'

        minutes_ago = int((datetime.utcnow().timestamp() - self.start_timestamp) / 60)
        description += f'Время: **{minutes_ago} минут назад**\n'
        description += f'Результат: **{self.battle.get_result_text().upper()}**'

        trophy_change = 0
        if self.battle.trophy_change is not None:
            trophy_change = self.battle.trophy_change
            description += f' ({trophy_change} кубков)'

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
