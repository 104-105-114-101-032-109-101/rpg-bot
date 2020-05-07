import discord
from random import randint, choice


with open('token.txt', 'r') as f:
    token = f.readline()

with open("players.txt", "r", encoding="utf8") as players_file:
    names_and_ids = [(pair.split()) for pair in players_file.readlines()]

players = [pair[1] for pair in name_and_id]

names = {pair[0]: pair[1:] for pair in names_and_ids}

skills = ["accounting", "anthopology", "appraise", "archaeology", "art craft", "charm", "climb", "credit rating",
          "cthulhu mythos", "disguise", "dodge", "drive auto", "elec repair", "fast talk", "fighting brawl",
          "firearms handgun", "firearms rifle shotgun", "first aid", "history", "intimidate", "jump", "language", "law",
          "library use", "listen", "locksmith", "mech repair", "medicine", "natural world", "navigate", "occult",
          "op hv machine", "persuade", "pilot", "psychology", "psychoanalysis", "ride", "science", "sleight of hand",
          "spot hidden", "stealth", "survival", "swim", "throw", "track"
          ]

insults = [", foca no jogo, porra", "para de fazer merda por um minuto", ", anda logo!", " fodeu a sessão"
           ", daqui a pouco o mestre vai provocar um acidente para acabar logo com isso", " tem que ser expulso!"
           " só consegue ir atrás de champola no RPG mesmo", ", você se sairia melhor como NPC",
           ", tinha que deixar para preparar as coisas na última hora né, animal!", " tem alinhamento chaotic merda",
           " jamais terá a capacidade intelectual para ser mestre"]

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(ctx):
    try:
        channel = discord.utils.get(client.get_all_channels(), name='geral')
        role = discord.utils.get(ctx.guild.roles, name = "personagem-pendente")
        await ctx.add_roles(role)
        await channel.send("Seja bem-vindo, Deputado!")
    except Exception:
        print("DEU MERDA NO MEMBER JOIN")

@client.event
async def on_message(message):
    global game_started

    if message.author == client.user:
        return

    channel = message.channel
    content = message.content.strip().lower()

    # Hello There
    if names["bot"] in content:
        await channel.send("Sou eu!")
        return

    # Prevent from unnecessary reading
    if not content.startswith("!"):
        return

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
        return

    # Do test
    if content.startswith('!teste') and (channel.name == "dev-bot" or channel.name == "rolar-dados"):
        separate = True
        func = min
        if content.endswith("-v"):
            die_units = randint(0, 9)
            die_tens = randint(0, 9)
            die_tens_2 = randint(0, 9)
            content = content[:-2]
            result_type = "Resultado com vantagem"
            result = func(die_tens, die_tens_2)*10 + die_units
        elif content.endswith("-d"):
            die_units = randint(0, 9)
            die_tens = randint(0, 9)
            die_tens_2 = randint(0, 9)
            content = content[:-2]
            result_type = "Resultado com desvantagem"
            func = max
            result = func(die_tens, die_tens_2)*10 + die_units
        else:
            die_units = randint(0, 9)
            die_tens = randint(0, 9)
            result_type = "Resultado"
            separate = False
            result = die_tens*10 + die_units
        modifier = 0
        if content.strip() != '!teste':
            modifier = int(content.replace(" ", "")[6:])

        if result == 0:
            result = 100

        if separate:
            await channel.send("{}:\n\t1d10 unidades = {}\n\t2d10 dezenas = {}({}, {}) = {}\n\tTotal = {}+({}) = **{}**".format(
                                result_type, die_units, func.__name__, die_tens, die_tens_2, func(die_tens, die_tens_2),
                                result, modifier, result + modifier))
        else:
            await channel.send("{}: \n\t1d10 unidades = {}\n\t1d10 dezenas = {}\n\tTotal = {}+({}) = **{}**".format(
                                result_type, die_units, die_tens, result, modifier, result + modifier))

        # beta version
        if die_tens == 9 or result == 100:
            await channel.send("se fudeu")
        elif die_tens == 0:
            await channel.send("cagão da porra")

        return

    # Roll dice
    if content.startswith('!roll') and (channel.name == "dev-bot" or channel.name == "rolar-dados"):
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
            await channel.send("Total d{}:  **{}**\t\t{}\n\nTotal d{}:  **{}**\t\t{}".format(face_num, total, results,
                                                                                     add_face_num, add_total,
                                                                                     add_results))
        else:
            await channel.send("Total:  **{}**\t\t{}".format(total, results))
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

    # TODO: change to Role authentication instead
    if (content.startswith('!abrir') or content.startswith("!open")) and (str(message.author.id) == names["rodrigo"] or str(message.author.id) == names["nicholas"]):
        if not game_started:
            game_started = True
            with open("success.txt", "a") as file:
                file.write("open session\n")
            await channel.send("A sessão está aberta!")
        else:
            await channel.send("A sessão já estava aberta")
        return

    if (content.startswith('!fechar') or content.startswith("!close")) and (str(message.author.id) == names["rodrigo"] or str(message.author.id) == names["nicholas"]):
        if game_started:
            game_started = False
            with open("success.txt", "r") as success_file:
                file_content = success_file.readlines()
                last_session_rolls = []
                for line in reversed(file_content):
                    if "open session" in line:
                        break
                    else:
                        last_session_rolls.append(line)
            with open("success.txt", "a") as success_file:
                success_file.write("close session\n")

            # TODO: deal with the 2000 character limit may be necessary, but this won't happen in most cases
            if len(last_session_rolls) > 0:
                await channel.send("Nesta sessão, os jogadores tiveram os seguintes sucessos")
                await channel.send("\n".join(last_session_rolls))
                return
            else:
                await channel.send("Nenhum teste de perícia foi detectado")
                return
        else:
            await channel.send("A sessão não estava aberta")

    # Skill List
    if content.startswith("!skills"):
        await channel.send("```" + " --- ".join(skills) + "```")

    # Skill Test
    skill_command = [argument.strip() for argument in content.split()]
    skill_name = skill_command[0][1:]
    skill_value = skill_command[-1]
    for skill in skills:
        if skill_name == skill:
            if skill_value.isnumeric():
                base_value = abs(int(skill_value))
                separate = True
                func = min
                if "-v" in skill_command:
                    die_units = randint(0, 9)
                    die_tens = randint(0, 9)
                    die_tens_2 = randint(0, 9)
                    content = content[:-2]
                    result_type = f"Teste de {skill} com vantagem"
                    result = func(die_tens, die_tens_2) * 10 + die_units
                elif "-d" in skill_command:
                    die_units = randint(0, 9)
                    die_tens = randint(0, 9)
                    die_tens_2 = randint(0, 9)
                    content = content[:-2]
                    result_type = f"Teste de {skill} com desvantagem"
                    func = max
                    result = func(die_tens, die_tens_2) * 10 + die_units
                else:
                    die_units = randint(0, 9)
                    die_tens = randint(0, 9)
                    result_type = f"Teste de {skill}"
                    separate = False
                    result = die_tens * 10 + die_units

                if result == 0:
                    result = 100

                if separate:
                    await channel.send(
                        "{}:\n\t1d10 unidades = {}\n\t2d10 dezenas = {}({}, {}) = {}\n\tTotal = **{}**".format(
                            result_type, die_units, func.__name__, die_tens, die_tens_2, func(die_tens, die_tens_2),
                            result))
                else:
                    await channel.send(
                        "{}: \n\t1d10 unidades = {}\n\t1d10 dezenas = {}\n\tTotal = **{}**".format(
                            result_type, die_units, die_tens, result))

                # Fracasso
                if result > base_value:
                    await channel.send("Falhou no teste")
                # Sucesso
                else:
                    if result == base_value:
                        await channel.send("Na risca!")
                    elif die_tens == 0:
                        await channel.send("Cagão da porra")
                    else:
                        await channel.send("Passou no teste")
                    if game_started:
                        with open("success.txt", "r") as success_file:
                            file_content = success_file.readlines()
                            session_content = []
                            print(file_content)
                            for line in reversed(file_content):
                                if "open session" in line:
                                    break
                                else:
                                    session_content.append(line)
                            print(session_content)
                        with open("success.txt", "a") as success_file:
                            if f"<@!{message.author.id}> {skill_name}" not in session_content:
                                success_file.write(f"<@!{message.author.id}> {skill_name}\n")
                            else:
                                await channel.send(f"Você já teve um sucesso de {skill} nesta sessão!")
                    else:
                        await channel.send("Este teste foi feito fora de uma sessão. O <@&678994632612380672> precisa `!abrir` a sessão para que o teste seja registrado")
                return
            else:
                await channel.send("Verifique se a sintaxe está correta: "
                                   "`![nome da pericia] -[v/d] [valor base da pericia]` Para uma lista das skills,"
                                   " use o comando **!skills**")
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
                           "\n\t*Exemplo simples:*\n\t`!teste -2` rola 1d100 e subtrai 2 do resultado"
                           "\n\n\t*Exemplo com vantagem:*\n\t`!teste +5 -v` rola 3d10, escolhe o menor dado para as dezenas"
                           " e soma 5 ao resultado\n\n\t*Exemplo com desvantagem:*\n\t`!teste -7 -d` rola 3d10,"
                           " escolhe o maior dado para as dezenas e subtrai 7 do resultado"
                           "\n\n\n**![nome da pericia] [valor base da pericia]**: Faz um teste de perícia, e avisa quais perícias o jogador teve sucesso no final da sessão"
                           "\n\t*Exemplo simples:*\n\t`!accounting 38` faz um teste de accounting"
                           "\n\n\t*Exemplo com vantagem:*\n\t`!law -v 69` faz um teste de law e escolhe o menor dado para as dezenas"
                           "\n\n\t*Exemplo com desvantagem:*\n\t`!disguise -d 72` faz um teste de disguise e escolhe o maior dado para as dezenas"
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
                           "\n\n\n**!abrir/!fechar**: Comandos apenas acessíveis ao mestre, definem quando começa ou termina uma sessão"
                           "\n\n\n**!skills**: Mostra a lista de perícias existentes no jogo"
                           "\n\n\n**!help**: Mostra os comandos do bot")
        return

    # No command detected, it probably was a skill attempt
    await channel.send("Não reconheci esse comando. Se você tentou fazer um teste de skill, verifique se a sintaxe está correta: "
                       "```![nome da pericia] -[v/d] [valor base da pericia]```Para uma lista das skills, use o comando **!skills**")
    return


client.run(token)
