"""Events to trigger actions."""

from datetime import datetime
import logging
import string

import discord
from discord.ext.commands import Cog, Context

from obsidion import constants
from obsidion.bot import Obsidion

log = logging.getLogger(__name__)

ALLOWED_CHARS = string.ascii_letters + string.digits + "_"


class Events(Cog):
    """Events cog."""

    def __init__(self, bot: Obsidion) -> None:
        """Init."""
        self.bot = bot

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        """On a guild joining."""
        if constants.Channels.new_guild_channel:
            embed = discord.Embed(name=f"{self.bot.user.name} has joined a guild")
            embed.set_footer(
                text=(
                    f"Guild: {len(self.bot.guilds):,} | Shard: "
                    f"{guild.shard_id}/{self.bot.shard_count-1}"
                )
            )
            guild_text = (
                f"Name: `{guild.name}`\n"
                f"ID: `{guild.id}`\n"
                f"Owner ID: `{guild.owner.id}`\n"
            )

            embed.add_field(name="Guild", value=guild_text)
            embed.add_field(name="Region", value=guild.region)
            embed.timestamp = datetime.now()
            if guild.icon_url:
                embed.set_thumbnail(url=guild.icon_url)
            else:
                embed.set_thumbnail(url="https://i.imgur.com/AFABgjD.png")
            channel = self.bot.get_channel(constants.Channels.new_guild_channel)
            await channel.send(embed=embed)

    @Cog.listener()
    async def on_command_completion(self, ctx: Context) -> None:
        """Report completed commands to statsd."""
        command_name = ctx.command.qualified_name.replace(" ", "_")

        self.bot.stats.incr(f"commands.{command_name}")


def setup(bot: Obsidion) -> None:
    """Add `News` cog."""
    bot.add_cog(Events(bot))