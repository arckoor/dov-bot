-- CreateTable
CREATE TABLE "GuildConfig" (
    "id" SERIAL NOT NULL,
    "guild" BIGINT NOT NULL,
    "guild_log" BIGINT,
    "time_zone" TEXT DEFAULT 'UTC',

    CONSTRAINT "GuildConfig_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "PhraseConfig" (
    "id" SERIAL NOT NULL,
    "guild" BIGINT NOT NULL,

    CONSTRAINT "PhraseConfig_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AssignedPhrase" (
    "id" SERIAL NOT NULL,
    "guild" BIGINT NOT NULL,
    "phrase" TEXT NOT NULL,
    "role" BIGINT NOT NULL,
    "match_case" BOOLEAN NOT NULL DEFAULT false,
    "phraseConfigId" INTEGER NOT NULL,

    CONSTRAINT "AssignedPhrase_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "GuildConfig_guild_key" ON "GuildConfig"("guild");

-- CreateIndex
CREATE INDEX "GuildConfig_guild_idx" ON "GuildConfig"("guild");

-- CreateIndex
CREATE UNIQUE INDEX "PhraseConfig_guild_key" ON "PhraseConfig"("guild");

-- CreateIndex
CREATE INDEX "PhraseConfig_guild_idx" ON "PhraseConfig"("guild");

-- AddForeignKey
ALTER TABLE "AssignedPhrase" ADD CONSTRAINT "AssignedPhrase_phraseConfigId_fkey" FOREIGN KEY ("phraseConfigId") REFERENCES "PhraseConfig"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
