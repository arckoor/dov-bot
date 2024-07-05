from prisma import Prisma, models


db = None


async def connect():
    global db
    db = Prisma()
    await db.connect()


async def disconnect():
    global db
    await db.disconnect()


async def get_guild_config(id: int) -> models.GuildConfig:
    global db
    return await db.guildconfig.upsert(
        where={
            "guild": id
        },
        data={
            "create": {
                "guild": id
            },
            "update": {
            }
        },
    )


async def get_phrase_config(id: int) -> models.PhraseConfig:
    global db
    return await db.phraseconfig.upsert(
        where={
            "guild": id
        },
        data={
            "create": {
                "guild": id
            },
            "update": {
            }
        },
        include={
            "assigned_phrases": True
        }
    )
