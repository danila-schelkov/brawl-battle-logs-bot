import asyncio
import time
from datetime import datetime

import discord
from discord.ext import commands

from brawlstats_api import get_new_battle_logs, BattleLog
from database import profiles_database
from models.profile import Profile
from utilities import config

CHECK_INTERVAL = 60 * 5

start_time = time.time()

intents = discord.Intents.default()
bot = commands.Bot('/', intents=intents)


async def on_ready():
    print(f'{bot.user.name} loaded in {time.time() - start_time:.2f}сек.')

    if not config.initialized:
        config.initialized = True
        return

    await check_new_battles()


async def check_new_battles():
    """Sends all recent battles to post channel

    :return:
    """
    channel_to_post: discord.TextChannel = bot.get_channel(config.post_channel)

    while True:
        profiles: list[Profile] = profiles_database.get_all()
        for profile in profiles:
            update_needed = False

            battle_logs: list[BattleLog] = get_new_battle_logs(profile.get_tag(), profile.last_battle_timestamp)
            for battle_log in battle_logs:
                own_player, own_team = battle_log.battle.get_player_and_team(profile)

                description, trophy_change = battle_log.get_battle_description(
                    own_player,
                    own_team
                )

                embed = create_battle_embed(description, battle_log.battle.get_result_text(), trophy_change)

                await channel_to_post.send(embed=embed)

                if battle_logs.index(battle_log) == len(battle_logs) - 1:
                    profile.last_battle_timestamp = battle_log.start_timestamp
                    update_needed = True

            if update_needed:
                profiles_database.update(profile)

        await asyncio.sleep(CHECK_INTERVAL)


def create_battle_embed(description: str, battle_result: str, trophy_change: int) -> discord.Embed:
    embed = discord.Embed()
    embed.description = description
    embed.set_footer(text=f'Today at {datetime.now().strftime("%H:%M")}')
    if battle_result == 'victory' or trophy_change > 0:
        embed.colour = discord.Color.dark_green()
    elif battle_result == 'defeat' or trophy_change < 0:
        embed.colour = discord.Color.red()

    return embed


async def on_message(message: discord.Message, *args):
    channel: discord.TextChannel = message.channel
    print(channel.id, message.content)


async def on_command_error(context, exception):
    pass


def main():
    bot.add_listener(on_ready)
    bot.add_listener(on_message)

    bot.add_listener(on_command_error)
    bot.run(config.discord_bot_token)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
