# Bot URL: https://discordapp.com/api/oauth2/authorize?client_id=535962207083692063&permissions=8&scope=bot
import os
import re
import discord
from discord.ext import commands

from cr_parser_lib import *

prefix = "?"
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")

TOKEN = "NTM1OTYyMjA3MDgzNjkyMDYz.DyPybw.kh-lUvrh-0SDTWkXpqpunibWIMU"

server_data_dir = "data"
crs_data_dir = "crs"


# Bot events
@bot.event
async def on_ready():
    print("Bot is ready, waiting for your command.")


@bot.event
async def on_message(message):
    is_bot = message.author.bot
    if is_bot:
        return 0
    else:
        message_content = message.content
        if len(message_content) < 700 and not (
                message_content.startswith("{}war".format(prefix)) or message_content.startswith(
            "{}usage".format(prefix))):
            return 0
        else:
            if message_content.startswith("{}usage".format(prefix)):
                channel = message.channel
                embed = discord.Embed(
                    title="**Bot for calculating damage received automatically when you post CRs in alliance war**\n",
                    color=discord.Color.blue(),
                    description=""
                )

                embed.description += "__**Bot usage:**__\n \
                                      **{prefix}usage** - This command, show bot usage.\n\n \
                                      **{prefix}war** <alliance name> <alliance name> <cr channel>\n \
                                       Ex: {prefix}war -IKS- DWOOD #iks-vs-dwood\n\n \
                                       __**Note:**__\n \
                                       - run this command ONCE before post the CRs.\n \
                                       - alliance name MUST be exactly the name which is displayed in the CRs, for example: -IKS-, BONE, DWOOD, etc\n \
                                       - cr channel MUST be created before use this command.".format(prefix=prefix)

                await bot.send_message(channel, embed=embed)

            elif message_content.startswith("{}war".format(prefix)):
                args = message_content.split()
                if len(args) != 4:
                    channel = message.channel
                    await bot.send_message(channel, "Invalid command.\nSyntax: `{}war <alliance name> <alliance name> <cr channel>`".format(prefix))
                else:
                    # Create a crs config file
                    clan1 = args[1]
                    clan2 = args[2]
                    crs_channel = re.search(r"<#(\d+)>", args[3]).groups()[0]
                    crs_config_name = "{}-vs-{}-{}".format(clan1, clan2, crs_channel)
                    crs_file = "{}{}{}.json".format(crs_data_dir, os.sep, crs_config_name)
                    crs_file_content = {}
                    crs_file_content[clan1] = 0
                    crs_file_content[clan2] = 0
                    crs_file_content = json.dumps(crs_file_content)
                    if not os.path.exists(crs_file):
                        with open(crs_file, "w") as file:
                            file.write(crs_file_content)
            else:
                channel = message.channel
                this_channel_id = channel.id
                channel_list = {}
                for crs_file in os.listdir(crs_data_dir):
                    channel_id = re.search(r"(\d+)", crs_file)
                    if channel_id is not None:
                        channel_list[channel_id.groups()[0]] = crs_file
                if this_channel_id not in channel_list.keys():
                    return 0
                else:
                    atk, dfd, pts_change, cr_result = crParse(crs_data_dir + os.sep + channel_list[this_channel_id],
                                                              message_content)

                    embed = discord.Embed(
                        title="**[{}] vs [{}]:**\n".format(atk, dfd),
                        color=discord.Color.blue(),
                        description=""
                    )

                    embed.description += "**CR Damage Received**\n[{}]: {:,}\n[{}]: {:,}\n\n".format(atk,
                                                                                                     pts_change[atk],
                                                                                                     dfd,
                                                                                                     pts_change[dfd])
                    embed.description += "**Total Damage Received**\n[{}]: {:,}\n[{}]: {:,}\n".format(atk,
                                                                                                      cr_result[atk],
                                                                                                      dfd,
                                                                                                      cr_result[dfd])

                    await bot.send_message(channel, embed=embed)


# ------------------------------------------------------
if __name__ == "__main__":
    bot.run(TOKEN)
