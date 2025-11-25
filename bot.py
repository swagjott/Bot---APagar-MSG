import discord
from discord.ext import commands
import asyncio
import re

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Lista de usuários autorizados
allowed_users = set()

# --------------------
# Função: converter tempo
# --------------------
def parse_time(t):
    match = re.match(r"(\d+)([smhd])$", t)
    if not match:
        return None
    
    value = int(match.group(1))
    unit = match.group(2)

    if unit == "s":
        return value
    if unit == "m":
        return value * 60
    if unit == "h":
        return value * 3600
    if unit == "d":
        return value * 86400


# --------------------
# Comando: permitir usuário
# --------------------
@bot.command()
async def permitir(ctx, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        allowed_users.add(user.id)
        await ctx.send(f"✅ {user.mention} agora pode usar o bot.")
    else:
        await ctx.send("❌ Você precisa ser ADMINISTRADOR.")


# --------------------
# Comando: remover permissão
# --------------------
@bot.command()
async def negar(ctx, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        allowed_users.discard(user.id)
        await ctx.send(f"⛔ {user.mention} perdeu a permissão.")
    else:
        await ctx.send("❌ Você precisa ser ADMINISTRADOR.")


# --------------------
# VIEW COM OS BOTÕES
# --------------------
class DeleteOptions(discord.ui.View):
    def __init__(self, msg):
        super().__init__(timeout=60)
        self.msg = msg

    @discord.ui.button(label="Segundos (s)", style=discord.ButtonStyle.blurple)
    async def sec(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Digite a quantidade de segundos:", ephemeral=True)

        def check(m):
            return m.author.id == interaction.user.id and m.channel == interaction.channel

        msg = await bot.wait_for("message", check=check)
        seconds = parse_time(msg.content + "s")

        await asyncio.sleep(seconds)
        await self.msg.delete()

    @discord.ui.button(label="Minutos (m)", style=discord.ButtonStyle.green)
    async def min(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Digite a quantidade de minutos:", ephemeral=True)

        def check(m):
            return m.author.id == interaction.user.id and m.channel == interaction.channel

        msg = await bot.wait_for("message", check=check)
        seconds = parse_time(msg.content + "m")

        await asyncio.sleep(seconds)
        await self.msg.delete()

    @discord.ui.button(label="Horas (h)", style=discord.ButtonStyle.gray)
    async def hour(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Digite a quantidade de horas:", ephemeral=True)

        def check(m):
            return m.author.id == interaction.user.id and m.channel == interaction.channel

        msg = await bot.wait_for("message", check=check)
        seconds = parse_time(msg.content + "h")

        await asyncio.sleep(seconds)
        await self.msg.delete()

    @discord.ui.button(label="Dias (d)", style=discord.ButtonStyle.red)
    async def day(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Digite a quantidade de dias:", ephemeral=True)

        def check(m):
            return m.author.id == interaction.user.id and m.channel == interaction.channel

        msg = await bot.wait_for("message", check=check)
        seconds = parse_time(msg.content + "d")

        await asyncio.sleep(seconds)
        await self.msg.delete()

    @discord.ui.button(label="Não apagar", style=discord.ButtonStyle.green)
    async def no_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("👌 A mensagem **não será apagada**.", ephemeral=True)
        self.stop()


# --------------------
# Comando principal: !tempmsg
# --------------------
@bot.command()
async def tempmsg(ctx, *, texto=None):

    # Verifica permissão
    if ctx.author.id not in allowed_users:
        return await ctx.send("❌ Você **não tem permissão** para usar este comando.")

    if texto is None:
        return await ctx.send("Use: `!tempmsg sua mensagem`")

    # Cria o embed
    embed = discord.Embed(
        title="⏳ Mensagem Configurável",
        description=texto,
        color=discord.Color.blue()
    )

    msg = await ctx.send(embed=embed, view=DeleteOptions(None))

    # Passa a msg para a View
    view = DeleteOptions(msg)
    await msg.edit(view=view)


# --------------------
# RODAR O BOT
# --------------------
bot.run("SEU_TOKEN_AQUI")
