import discord
from random import randint, choice


with open('C:\\Users\\Nicholas\\Discord-Bots\\tokens\\rpg-bot.txt', 'r') as f:
    token = f.readline()

with open("players.txt", "r", encoding="utf8") as players_file:
    names_and_ids = [(pair.split()) for pair in players_file.readlines()]

players = [pair[1] for pair in name_and_ids]

names = {pair[0]: pair[1:] for pair in names_and_ids}

insults = [", foca no jogo, porra", "para de fazer merda por um minuto", ", anda logo!", " fodeu a sessão"
           ", daqui a pouco o mestre vai provocar um acidente para acabar logo com isso", " tem que ser expulso!"
           " só consegue ir atrás de champola no RPG mesmo", ", você se sairia melhor como NPC"]

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    content = message.content.strip().lower()

    # Insult
    if content.startswith('!insulto'):
        insult = choice(insults)
        if content.endswith('!insulto'):
            player = choice(players)
        else:
            content = content.replace(" ", "")[8:]
            try:
                player = names[content]
            except KeyError:
                player = content
                await channel.send('{} {}'.format(player, insult))
                return
        await channel.send('<@!{}> {}'.format(player, insult))

    # Do test
    if content.startswith('!teste') and (channel.name == "desenvolvimento-bot" or channel.name == "rolar-dados"):
        if content.endswith("-v"):
            die = max(randint(1, 20), randint(1, 20))
            content = content[:-2]
            result_type = "Resultado com vantagem"
        elif content.endswith("-d"):
            die = min(randint(1, 20), randint(1, 20))
            content = content[:-2]
            result_type = "Resultado com desvantagem"
        else:
            die = randint(1, 20)
            result_type = "Resultado"

        modifier = 0
        if content != '!teste':
            modifier = int(content.replace(" ", "")[6:])
        await channel.send("{}:  {}+({}) = {}".format(result_type, die, modifier, die + modifier))
        return

    # Roll dice
    if content.startswith('!roll') and (channel.name == "desenvolvimento-bot" or channel.name == "rolar-dados"):
        content = content.replace(" ", "")[5:]

        modifier, dice_num, face_num, additional_flag = 0, 0, 0, 0
        add_modifier, add_dice_num, add_face_num, add_total = 0, 0, 0, 0
        add_results = []

        # If there is an additional die
        if content.find('and') != -1:
            additional_flag = 1
            content, additional = content.split('and')

            if additional.find('+') != -1:
                additional, add_modifier = additional.split('+')
            elif additional.find('-') != -1:
                additional, add_modifier = additional.split('-')
                add_modifier = "-" + add_modifier
            if additional.find('d') != -1:
                add_dice_num, add_face_num = additional.split('d')

            add_modifier = int(add_modifier)
            add_dice_num = int(add_dice_num)
            add_face_num = int(add_face_num)

            add_results = []
            add_total = add_modifier
            for die in range(add_dice_num):
                add_result = randint(1, add_face_num)
                add_total += add_result
                add_results.append(add_result)

            add_results = sorted(add_results)

        if content.find('+') != -1:
            content, modifier = content.split('+')
        elif content.find('-') != -1:
            content, modifier = content.split('-')
            modifier = "-" + modifier
        if content.find('d') != -1:
            dice_num, face_num = content.split('d')

        modifier = int(modifier)
        dice_num = int(dice_num)
        face_num = int(face_num)

        results = []
        total = modifier
        for die in range(dice_num):
            result = randint(1, face_num)
            total += result
            results.append(result)

        results = sorted(results)
        # TODO: add "cagão da porra" when it results in 20/1d20 and
        #  "tomou no cu" when 1/1d20 (also implement for !teste)
        if additional_flag:
            await channel.send("Total d{}:  {}\t\t{}\n\nTotal d{}:  {}\t\t{}".format(face_num, total, results,
                                                                                     add_face_num, add_total,
                                                                                     add_results))
        else:
            await channel.send("Total:  {}\t\t{}".format(total, results))
        return

    # Turn Off
    if content.startswith('!dorme'):
        await channel.send("Boa noite!")
        await client.close()
        return

    # Random name generator (alternate between a list A and a list B in which
    if content.startswith('!random'):
        consonants = [chr(i+97) for i in range(26)] + ["bl", "gr", "fl", "fr", "ch", "sh", "br", "pr", "tr", "th", "pl"]
        vowels = ["a", "e", "i", "o", "u"]
        consonants = [x for x in consonants if x not in vowels]
        length = 5
        long = False
        if not content.endswith('!random'):
            length = int(content.split()[-1])
            if not (0 < length < 201):
                long = True
                await channel.send("Esta aí é longa demais ( ͡° ͜ʖ ͡°)")
        if not long:
            word = ""
            for x in range(length):
                word += str(consonants[randint(0, 26)] if x % 2 == 0 else vowels[randint(0, 4)])
            await channel.send(word)
            return

    # Help
    if content.startswith('!help'):
        await channel.send("**!roll**: Rola um ou mais dados\n\t*Exemplo simples:*"
                           "\n\t`!roll 6d20` rola 6 dados de 20 faces\n\n\t"
                           "*Exemplo com modificador:*\n\t`!roll 1d20 -3`"
                           " rola 1 dado de 20 faces e subtrai 3 do resultado"
                           "\n\n\t*Exemplo com mais dados:*\n\t`!roll 2d20 +5 and 2d6` rola 2 dados de 20 faces e "
                           "adiciona 5 ao resultado. Depois, rola 2 dados de 6 faces\n\n\n"
                           "**!teste**: Faz um teste de perícia"
                           "\n\t*Exemplo simples:*\n\t`!teste -2` rola 1d20 e subtrai 2 do resultado"
                           "\n\n\t*Exemplo com vantagem:*\n\t`!teste +5 -v` rola 2d20, escolhe o maior dado"
                           " e soma 5 ao resultado\n\n\t*Exemplo com desvantagem:*\n\t`!teste +1 -d` rola 2d20,"
                           " escolhe o menor dado e soma 1 ao resultado"
                           "\n\n\n**!insulto**: Faz um insulto randômico a um jogador"
                           "\n\t*Exemplo simples:*\n\t`!insulto` escolhe um jogador aleatoriamente"
                           "\n\n\t*Exemplo direcionado:* "
                           "\n\t`!insulto bullywug` faz um insulto direcionado ao nome \"bullywug\""
                           "\n\n\t*Exemplo direcionado a um jogador:* "
                           "\n\t`!insulto nicholas` notifica e insulta o jogador cujo primeiro nome é \"nicholas\""
                           "\n\n\n**!random**: Aleatoriamente gera uma palavra legível de 1 a 200 caracteres"
                           "\n\t*Exemplo simples:*\n\t`!random` gera uma palavra aleatória de 5 letras"
                           "\n\n\t*Exemplo com tamanho variável:* "
                           "\n\t`!random 14` gera uma palavra aleatória de 14 letras"
                           "\n\n\n**!dorme**: Desliga o bot (é necessário fazer isso quando não forem mais usá-lo)"
                           "\n\n\n**!help**: Mostra os comandos do bot")


client.run(token)
# mover para outro canal ao falar merda
# await move_to(channel)
