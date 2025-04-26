import discord
from discord.ext import commands
import random
from discord import app_commands
import asyncio


# Inicializando o bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento para quando o bot estiver pronto
@bot.event
async def on_ready():
    print(f'Bot {bot.user} está online!')


@bot.tree.command(name="sorteio", description="Sorteia uma pessoa do canal de voz e envia o resultado no canal de texto escolhido.")
@app_commands.describe(canal_texto="Escolha o canal de texto para enviar o resultado do sorteio.",
                       num_sorteados="Número de pessoas a serem sorteadas.")
async def sorteio(interaction: discord.Interaction, canal_texto: discord.TextChannel, num_sorteados: int):
    await interaction.response.defer(thinking=False)

    if interaction.user.voice:
        canal = interaction.user.voice.channel

        membros = [membro for membro in canal.members if not membro.bot]

        if membros:
            # Se for sortear mais de uma pessoa
            if num_sorteados > 1:
                if num_sorteados > len(membros):
                    await interaction.followup.send(f'O número de sorteados não pode ser maior que o número de membros no canal ({len(membros)} membros).')
                    return

                # Criar mensagem inicial com o número de sorteados
                await canal_texto.send(f'📢 {num_sorteados} pessoas serão sorteadas!')

                mensagem = await canal_texto.send(f'🎲 Preparando o sorteio... iniciando contagem regressiva!')

                await asyncio.sleep(5)

                # Mostrar lista de todos os participantes
                participantes = [membro.display_name for membro in membros]
                await canal_texto.send(f'Participantes do sorteio: {", ".join(participantes)}\n────────────────────────────')

                # Contagem regressiva de 10 segundos
                for i in range(10, 0, -1):
                    await mensagem.edit(content=f'⏳ Sorteio em: {i}...')
                    await asyncio.sleep(1)

                # Sorteio das pessoas, sem repetições
                vencedores = random.sample(membros, num_sorteados)

                # Atualizar a mensagem com os vencedores
                await mensagem.edit(content=f'🎉 Os 🦍 sorteados foram: **{", ".join([v.display_name for v in vencedores])}**, Parábens!')

                # Informar que o sorteio foi realizado
                await interaction.followup.send(f'O sorteio foi concluído e o resultado foi enviado para {canal_texto.mention}')

            #Sorteio para apenas 1 pessoa
            else:
                # Criar mensagem inicial com o número de sorteados
                await canal_texto.send(f'📢 {num_sorteados} pessoa será sorteada!')

                mensagem = await canal_texto.send(f'🎲 Preparando o sorteio... iniciando contagem regressiva!')

                await asyncio.sleep(5)

                # Mostrar lista de todos os participantes
                participantes = [membro.display_name for membro in membros]
                await canal_texto.send(f'Participantes do sorteio: {", ".join(participantes)}\n────────────────────────────')

                # Contagem regressiva de 10 segundos
                for i in range(10, 0, -1):
                    await mensagem.edit(content=f'⏳ Sorteio em: {i}...')
                    await asyncio.sleep(1)

                vencedor = random.choice(membros)
                await mensagem.edit(content=f'🎉 O 🦍 sorteado foi: **{vencedor.display_name}** Parabéns!')

                await interaction.followup.send(f'Resultado enviado no canal {canal_texto.mention} ✅')
        else:
            await interaction.followup.send('Não há membros suficientes no canal de voz para fazer o sorteio.')
    else:
        await interaction.followup.send('Você não está em um canal de voz!')


# Sincronizar os comandos com o servidor
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} está online e pronto!')

# Token do bot (substitua pelo seu token)
bot.run('COLAR TOQUEM AQUI')
