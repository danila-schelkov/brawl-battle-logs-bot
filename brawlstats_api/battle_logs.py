import brawlstats

from brawlstats_api.models.battle_log import BattleLog
from utilities import config

brawlstats_client = brawlstats.Client(config.brawl_stats_token)


def get_new_battle_logs(tag: str, timestamp: int) -> list[BattleLog]:
    """Returns a list of battle logs since the specified time.

    :param tag: account tag
    :param timestamp: timestamp since should add battle log to list
    :return:
    """

    battle_logs = []

    raw_battle_logs = brawlstats_client.get_battle_logs(tag).raw_data
    for battle_log_data in raw_battle_logs:
        battle_log: BattleLog = BattleLog.wrap(battle_log_data)

        if battle_log.start_timestamp <= timestamp:
            break

        if battle_log.battle.type == 'challenge':
            continue

        battle_logs.append(battle_log)

    return battle_logs[::-1]
