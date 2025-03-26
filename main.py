import discord
from discord.ext import commands, tasks
import os
import asyncio
from datetime import datetime, timedelta
from keep_alive import keep_alive
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class MeuBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot conectado como {self.bot.user}')
        self.enviar_mensagem.start()

    @tasks.loop(hours=24)
    async def enviar_mensagem(self):
        channel = self.bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("Acordem bem!")

    @enviar_mensagem.before_loop
    async def antes_de_comecar(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(self.tempo_ate_6h())

    def tempo_ate_6h(self):
        agora = datetime.now()
        proximo_horario = agora.replace(hour=6, minute=0, second=0, microsecond=0)
        if agora >= proximo_horario:
            proximo_horario += timedelta(days=1)
        return (proximo_horario - agora).total_seconds()

bot.add_cog(MeuBot(bot))

keep_alive()

bot.run(TOKEN)
