import configparser
import time
from datetime import datetime

import discord
from discord.ext import commands
import brawlstats

from database.profiles import Profiles
from models.profile import Profile
from utilities import add_spaces

config = configparser.ConfigParser()
config.read('config.ini')

client = brawlstats.Client(config['brawl-stats']['token'])

start_time = time.time()
bot = commands.Bot('/')


async def on_ready():
    load_time = round(time.time() - start_time, 2)
    print(f'{bot.user.name} загружен за {load_time}сек.')

    profiles = Profiles()

    if not bool(int(config['DEFAULT']['initialized'])):
        config['DEFAULT']['initialized'] = '1'
        config.write(open('config.ini', 'w'))
        return

    channel_to_post: discord.TextChannel = bot.get_channel(int(config['channels']['post_channel']))
    while True:
        profile: Profile
        for profile in profiles.get_all():
            update_needed = False

            battle_logs: brawlstats.BattleLog = client.get_battle_logs(profile.tag)
            for battle_log in battle_logs.raw_data:
                timestamp = int(datetime.strptime(battle_log['battleTime'], '%Y%m%dT%H%M%S.000Z').timestamp())
                if timestamp <= profile.last_battle_timestamp:
                    break

                if 'type' in battle_log['battle'] and battle_log['battle']['type'] == 'challenge':
                    continue

                game_mode = battle_log['event']['mode']
                map_name = battle_log['event']['map']

                trophy_change = None
                if 'rank' in battle_log['battle']:
                    battle_result = str(battle_log['battle']['rank']) + ' место'
                else:
                    battle_result = battle_log['battle']['result']

                if 'trophyChange' in battle_log['battle']:
                    trophy_change = battle_log['battle']['trophyChange']

                own_player = None
                own_team = None
                if 'teams' in battle_log['battle']:
                    for team in battle_log['battle']['teams']:
                        for player in team:
                            if player['tag'][1:] == profile.tag:
                                own_player = player
                                own_team = team
                                break
                        if own_team is not None:
                            break
                elif 'players' in battle_log['battle']:
                    for player in battle_log['battle']['players']:
                        if player['tag'][1:] == profile.tag:
                            own_player = player
                            break

                player_name = own_player['name']
                brawler_name = own_player['brawler']['name']
                brawler_trophies = None
                if 'trophies' in own_player['brawler']:
                    brawler_trophies = own_player['brawler']['trophies']

                minutes_ago = int((datetime.utcnow().timestamp() - timestamp) / 60)

                embed = discord.Embed()
                embed.description = f'Игрок замечен в игре!\n'
                embed.description += f'**{player_name}** играл на **{brawler_name}**'
                
                if brawler_trophies is not None:
                    embed.description += f' на **{brawler_trophies}** кубках'
                embed.description += '\n'

                embed.description += f'Информация матча: \n'
                embed.description += f'Режим: **{add_spaces(game_mode)}**\n'
                embed.description += f'Карта: **{map_name}**\n'

                if own_team is not None:
                    embed.description += f'Команда:\n'
                    for player in own_team:
                        teammate_player_name = player['name']
                        teammate_brawler_name = player['brawler']['name'].capitalize()
                        
                        teammate_brawler_trophies = None
                        if 'trophies' in player['brawler']:
                            teammate_brawler_trophies = player['brawler']['trophies']

                        embed.description += f'**{teammate_brawler_name}** ({teammate_player_name}) '
                        if teammate_brawler_trophies is not None:
                            embed.description += f' на **{teammate_brawler_trophies}** кубков'
                        embed.description += '\n'

                embed.description += f'Результаты матча: \n'
                embed.description += f'Время: **{minutes_ago} минут назад**\n'
                embed.description += f'Результат: **{battle_result.upper()}**'
                if trophy_change is not None:
                    embed.description += f' ({trophy_change} кубков)'
                else:
                    trophy_change = 0

                embed.set_footer(text=f'Сегодня в {datetime.now().strftime("%H:%M")}')

                if battle_result == 'victory' or trophy_change > 0:
                    embed.colour = discord.Color.dark_green()
                elif battle_result == 'defeat' or trophy_change < 0:
                    embed.colour = discord.Color.red()

                await channel_to_post.send(embed=embed)

                if battle_logs.raw_data.index(battle_log) == 0:
                    profile.last_battle_timestamp = timestamp
                    update_needed = True

            if update_needed:
                profiles.update(profile)
        time.sleep(60 * 5)


async def on_message(message: discord.Message, *args):
    channel: discord.TextChannel = message.channel

    print(channel.id, message.content)


async def on_command_error(context, exception):
    pass


bot.add_listener(on_ready)
bot.add_listener(on_message)
bot.add_listener(on_command_error)
bot.run(config['discord']['token'])
