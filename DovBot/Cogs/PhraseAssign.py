import disnake # noqa
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from Cogs.BaseCog import BaseCog
from Database.DBConnector import db, get_phrase_config
from Views import Embed
from Util import Logging


class PhraseAssign(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.slash_command(name="phrase", description="Phrase assign management", dm_permission=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, send_messages=True, view_channel=True, manage_roles=True, read_messages=True)
    @commands.default_member_permissions(ban_members=True)
    async def phrase(self, inter: ApplicationCommandInteraction):
        pass

    @phrase.sub_command(name="list", description="List all phrases and their assigned roles.")
    async def list(self, inter: ApplicationCommandInteraction):
        phrase_config = await get_phrase_config(inter.guild_id)
        if len(phrase_config.assigned_phrases) == 0:
            await inter.response.send_message("No phrases are currently assigned.")
            return

        embed = Embed.default_embed(
            title="Phrases",
            description="All phrases and their assigned roles present in the server.",
            author=inter.author.name,
            icon_url=inter.author.avatar.url
        )

        for assigned_phrase in phrase_config.assigned_phrases:
            embed.add_field(
                name=f"ID: {assigned_phrase.id} | {assigned_phrase.phrase} | Match case: {assigned_phrase.match_case}",
                value=inter.guild.get_role(assigned_phrase.role).mention,
                inline=False
            )
        await inter.response.send_message(embed=embed)

    @phrase.sub_command(name="add", description="Add a phrase to the list.")
    async def add(
        self,
        inter: ApplicationCommandInteraction,
        phrase: str = commands.Param(description="The phrase to add to the list."),
        role: disnake.Role = commands.Param(description="The role to assign when the phrase is used."),
        match_case: bool = commands.Param(description="Whether the phrase should be case-sensitive.", default=False)
    ):
        phrase_config = await get_phrase_config(inter.guild_id)
        for assigned_phrase in phrase_config.assigned_phrases:
            if assigned_phrase.phrase == phrase and assigned_phrase.role == role.id:
                await inter.response.send_message("This combination of phrase and role is already present.", ephemeral=True)
                return

        await db.assignedphrase.create(
            data={
                "guild": inter.guild_id,
                "phrase": phrase,
                "role": role.id,
                "match_case": match_case,
                "PhraseConfig": {
                    "connect": {
                        "id": phrase_config.id
                    }
                }
            },
        )
        await Logging.guild_log(inter.guild_id, f"A phrase `{phrase}` was added with role {role.name} (`{role.id}`) by {inter.author.name} (`{inter.author.id}`).")
        await inter.response.send_message("Phrase added successfully.")

    @phrase.sub_command(name="remove", description="Remove a phrase from the list.")
    async def remove(
        self,
        inter: ApplicationCommandInteraction,
        id: int = commands.Param(description="The ID of the phrase to remove.")
    ):
        assigned_phrase = await db.assignedphrase.find_first(
            where={
                "id": id,
                "guild": inter.guild_id
            }
        )
        if assigned_phrase is None:
            await inter.response.send_message("This combination of phrase and role is not present.", ephemeral=True)
            return

        role = inter.guild.get_role(assigned_phrase.role)

        await db.assignedphrase.delete(
            where={
                "id": assigned_phrase.id
            }
        )
        await Logging.guild_log(inter.guild_id, f"A phrase `{assigned_phrase.phrase}` was removed with role {role.name} (`{role.id}`) by {inter.author.name} (`{inter.author.id}`).")
        await inter.response.send_message("Phrase removed successfully.")

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return

        phrase_config = await get_phrase_config(message.guild.id)
        for assigned_phrase in phrase_config.assigned_phrases:
            if not assigned_phrase.match_case:
                phrase = assigned_phrase.phrase.lower()
                content = message.content.lower()
            else:
                phrase = assigned_phrase.phrase
                content = message.content
            if phrase in content:
                await message.author.add_roles(message.guild.get_role(assigned_phrase.role), reason="Phrase assignment.")
                await Logging.guild_log(
                    message.guild.id, f"Assigned role {message.guild.get_role(assigned_phrase.role).name} to {message.author.name} (`{message.author.id}`) for phrase `{assigned_phrase.phrase}`."
                )


def setup(bot: commands.Bot):
    bot.add_cog(PhraseAssign(bot))
