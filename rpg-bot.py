import discord
from random import randint, choice

token = "INSERT TOKEN HERE"

players = ["350807294004559901", "469586367383601172", "363709396867481600", "350807294004559901", "350807294004559901",
           "596412080031006755", "363041660130557963"]

names = {"marlon":"350807294004559901", "pedro":"469586367383601172", "nicholas":"363709396867481600",
         "gabriel":"596412080031006755", "marcos":"363041660130557963", "bot":"596575148467945472"}

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
            player = names[content]
        await channel.send('<@!{}> {}'.format(player, insult))

    # Do test
    if content.startswith('!teste') and (channel.name == "desenvolvimento-bot" or channel.name == "rolar-dados"):
        modifier = 0
        if content != '!teste':
            modifier = int(content.replace(" ", "")[6:])
        die = randint(1, 20)
        await channel.send("Resultado:  {}+({}) = {}".format(die, modifier, die + modifier))

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

        if additional_flag:
            await channel.send("Total d{}:  {}\t\t{}\n\nTotal d{}:  {}\t\t{}".format(face_num, total, results,
                                                                                     add_face_num, add_total,
                                                                                     add_results))
        else:
            await channel.send("Total:  {}\t\t{}".format(total, results))

    # Turn Off
    if content.startswith('!dorme'):
        await channel.send("Boa noite!")
        await client.close()

    # Help
    if content.startswith('!help'):
        await channel.send("**!roll**: Rola um ou mais dados\n\t*Exemplo simples:*"
                           "\n\t`!roll 6d20` rola 6 dados de 20 faces\n\n\t"
                           "*Exemplo com modificador:*\n\t`!roll 1d20 -3`"
                           " rola 1 dado de 20 faces e subtrai 3 do resultado"
                           "\n\n\t*Exemplo com mais dados:*\n\t`!roll 2d20 +5 and 2d6` rola 2 dados de 20 faces e "
                           "adiciona 5 ao resultado. Depois, rola 2 dados de 6 faces\n\n\n"
                           "**!teste**: Faz um teste de perícia"
                           "\n\t*Exemplo:* `!teste +4` rola 1d20 e soma 4 ao resultado\n\n\n**!insulto**:"
                           "Faz um insulto randômico a um jogador\n\t*Exemplo simples:* `!insulto` escolhe um jogador"
                           "aleatoriamente\n\n\t*Exemplo direcionado:* "
                           "`!insulto nicholas` insulta o jogador cujo primeiro nome é \"nicholas\""
                           "\n\n\n**!dorme**: Desliga o bot (é necessário fazer isso quando não forem mais usá-lo)"
                           "\n\n\n**!help**: Mostra os comandos do bot")


client.run(token)
# mover Marlon para outro canal ao falar merda
# await move_to(channel)
