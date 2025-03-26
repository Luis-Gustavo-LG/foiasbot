import discord
from discord.ext import commands, tasks
import os
import asyncio
from datetime import datetime, timedelta
from keep_alive import keep_alive
import os
import pytz
from dotenv import load_dotenv

keep_alive()

# Carregar variáveis de ambiente
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
channel_id_str = os.getenv("CHANNEL_ID")

# Verifique se o valor não é None e se é um número válido
if channel_id_str is None or not channel_id_str.isdigit():
    raise ValueError("CHANNEL_ID não está definido ou é inválido. Certifique-se de definir corretamente a variável de ambiente.")

# Converta para inteiro
CHANNEL_ID = int(channel_id_str)

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
        await asyncio.sleep(self.tempo_ate_proximo_horario())  # Chamando a função que vai calcular o próximo horário

    def tempo_ate_proximo_horario(self):
        # Usando pytz para obter o horário local
        local_tz = pytz.timezone("America/Sao_Paulo")  # Substitua com o fuso horário de sua localidade
        agora = datetime.now(local_tz)
        print(f'Horário atual: {agora}')  # Debug para ver o horário atual

        # Defina o horário para o desejado (exemplo: 6h da manhã ou qualquer horário)
        proximo_horario = agora.replace(hour=6, minute=0, second=0, microsecond=0)

        # Se o horário já passou para hoje, ajusta para o próximo dia
        if agora >= proximo_horario:
            proximo_horario += timedelta(days=1)

        print(f'Próximo horário calculado: {proximo_horario}')  # Debug para ver o horário calculado

        # Calcular o tempo de espera até o próximo horário
        tempo_espera = (proximo_horario - agora).total_seconds()
        print(f'Esperando por {tempo_espera} segundos até o próximo horário.')
        return tempo_espera

class MeuBotPrincipal(commands.Bot):
    async def setup_hook(self):
        await self.add_cog(MeuBot(self))

# Criar instância do bot
bot = MeuBotPrincipal(command_prefix="!", intents=intents)

# Rodar o bot
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("Erro: DISCORD_TOKEN não foi encontrado nas variáveis de ambiente!")

bot.run(TOKEN)
