TOKEN = ''

import os
import asyncio
import discord
from discord import app_commands, Intents, Client, Interaction, Embed
from discord.ext import commands
import pyperclip
import colorsys
import random
import requests
from datetime import datetime
import spotipy
import spotipy.util as util
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Crear una instancia de Bot
intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name=".help",
        details="",
        image=""
    )
    await bot.change_presence(activity=activity)
    
    print(f'{bot.user.name} se ha conectado a discord')

def tiene_permisos(ctx, miembro):
    if miembro.top_role >= ctx.author.top_role:
        return False
    return True

@bot.command(help='Mostrar informacion acerca de un usuario en el servidor')
async def info(ctx, member: discord.Member=None):
    if not member:
        # Si no se menciona a nadie, mostrar la información del usuario que llama al comando
        member = ctx.author
    
    # Crear un objeto Embed
    embed = discord.Embed(title="Información del usuario", description=f"Esto es lo que sé de {member.mention}")

    # Agregar información del usuario
    embed.add_field(name="Nombre", value=member.name, inline=False)
    embed.add_field(name="Apodo", value=member.nick or "Ninguno", inline=False)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Fecha de creación de la cuenta", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Fecha de ingreso al servidor", value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Roles", value=",".join([role.mention for role in member.roles]), inline=False)
    embed.add_field(name="Estado", value=str(member.status).replace("online", "En línea").replace("idle", "Ausente").replace("dnd", "No molestar").replace("offline", "Desconectado"), inline=False)
    embed.add_field(name="Estado personalizado", value=member.activities[0].name if member.activities else "Ninguno", inline=False)

    
    
    if member.voice is not None:
        embed.add_field(name="Canal de voz actual", value=member.voice.channel.name, inline=False)
    # Agregar el avatar del usuario
    embed.set_thumbnail(url=member.avatar)
    # Enviar el Embed al canal donde se llamó el comando
    await ctx.send(embed=embed)


@bot.command(help='Crear un cartel con el texto que quieras')
async def cartel(ctx, *, texto):
    if not texto:
        await ctx.send("Debes proporcionar algún texto para crear un cartel.")
        return
    # abrir la imagen del cartel
    imagen = Image.open("cartel/cartel.png")

    # crear un objeto de dibujo para agregar el texto
    draw = ImageDraw.Draw(imagen)

    # especificar la fuente para el texto
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)

    # calcular el tamaño del texto
    texto_formateado = textwrap.fill(texto, width=15)
    texto_width, texto_height = draw.textsize(texto_formateado, font=font)

    # ajustar la caja delimitante en consecuencia
    x = 223
    y = 370
    width = 444
    height = 380
    padding = 0
    if texto_width > width - padding * 2:
        width = texto_width + padding * 2
    if texto_height > height - padding * 2:
        height = texto_height + padding * 2
    box = [(x, y), (x + width, y + height)]

    # calcular la posición vertical del texto para centrarlo verticalmente
    texto_y = y + ((height - texto_height) / 2) - 10  # ajuste de 10 píxeles para mejorar la apariencia visual

    # calcular la posición horizontal del texto para centrarlo horizontalmente
    texto_x = x + ((width - texto_width) / 2)

    

    # agregar el texto a la imagen dentro de la caja delimitante
    draw.text((texto_x, texto_y), texto_formateado, font=font, fill=(0, 0, 0), align='center')



    # guardar la imagen actualizada
    imagen.save("cartel/cartelnuevo.png")

    # enviar la imagen actualizada como un mensaje en Discord
    await ctx.send(file=discord.File("cartel/cartelnuevo.png"))

    # Borramos el archivo temporal
    os.remove("cartel/cartelnuevo.png")

@bot.command(help='Crear un meme del boton')
async def boton(ctx, *, input_str):
    # Divide la cadena de entrada en dos textos separados por una coma
    input_list = input_str.split(',')
    if len(input_list) != 2:
        await ctx.send('Por favor introduce dos textos separados por una coma')
        return

    text1, text2 = input_list[0].strip(), input_list[1].strip()
    text_size1 = (156, 72)
    text_pos1 = (86, 101)
    text_size2 = (147, 40)
    text_pos2 = (269, 69)

    # Carga la imagen
    image_path = os.path.join(os.getcwd(), 'boton', 'boton.jpg')
    img = Image.open(image_path)

    # Agrega el primer texto
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    text_width1, text_height1 = draw.textsize(text1, font=font1)
    text_pos1 = (text_pos1[0] + (text_size1[0] - text_width1) / 2, 
                 text_pos1[1] + (text_size1[1] - text_height1) / 2)
    draw.rectangle((text_pos1, (text_pos1[0] + text_size1[0], text_pos1[1] + text_size1[1])), fill=(255, 255, 255))
    draw.text(text_pos1, text1, font=font1, fill=(0, 0, 0))

    # Agrega el segundo texto
    font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    text_width2, text_height2 = draw.textsize(text2, font=font2)
    text_pos2 = (text_pos2[0] + (text_size2[0] - text_width2) / 2, 
                 text_pos2[1] + (text_size2[1] - text_height2) / 2)
    draw.rectangle((text_pos2, (text_pos2[0] + text_size2[0], text_pos2[1] + text_size2[1])), fill=(255, 255, 255))
    draw.text(text_pos2, text2, font=font2, fill=(0, 0, 0))

    # Guarda la imagen modificada y envíala al canal
    new_image_path = os.path.join(os.getcwd(), 'boton', 'modified.jpg')
    img.save(new_image_path)
    await ctx.send(file=discord.File(new_image_path))

    # Elimina la imagen modificada
    os.remove(new_image_path)
    
@bot.command(help='Comprar  usuarios con privilegios inferiores')
async def comprar(ctx, member: discord.Member):
    role_name = f"Propiedad de {ctx.author.name}"
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    
    if role is None:
        # Si el rol no existe, se crea y se guarda en la variable role
        role = await ctx.guild.create_role(name=role_name)
        
    if ctx.author.top_role > member.top_role:
        await member.add_roles(role)
        await ctx.send(f"{ctx.author.mention} ha comprado a {member.mention}. ¡Confirmado!")
    elif ctx.author.top_role == member.top_role:
        await ctx.send("Lo siento, no puedes comprar a alguien con los mismos privilegios que tú.")
    else:
        await ctx.send("Lo siento, no tienes suficientes privilegios para comprar a este usuario.")

@bot.command(help='Casarte alguien a quien menciones')
async def casar(ctx, member: discord.Member):
    # Crear mensaje y esperar 5 minutos para que la otra persona responda
    mensaje = await ctx.send(f"{member.mention}, ¿quieres casarte con {ctx.author.mention}? Tienes 5 minutos para responder con '.aceptar' o '.rechazar'.")
    try:
        def check(m):
            return m.author == member and m.content.lower() in ['.aceptar', '.rechazar']

        respuesta = await bot.wait_for('message', timeout=300.0, check=check)
    except asyncio.TimeoutError:
        await mensaje.edit(content=f"{member.mention} te ha ignorado. ¡La boda se ha cancelado!")
    else:
        if respuesta.content.lower() == '.aceptar':
            # Crear rol y agregarlo a ambos usuarios
            guild = ctx.guild
            roles = await guild.fetch_roles()  # obtener lista de roles en el servidor
            rol_name = f'casad@ con {member.name}'
            rol = discord.utils.get(roles, name=rol_name)  # buscar el rol en la lista de roles
            if rol is None:
                # Si el rol no existe, crearlo
                rol = await guild.create_role(name=rol_name)

            rol_name2 = f'casad@ con {ctx.author.name}'
            rol2 = discord.utils.get(roles, name=rol_name2)  # buscar el rol en la lista de roles
            if rol2 is None:
                # Si el rol no existe, crearlo
                rol2 = await guild.create_role(name=rol_name2)

            # Asignar el rol correspondiente a cada usuario
            await ctx.author.add_roles(rol)
            await member.add_roles(rol2)

            # Enviar mensaje de confirmación y un gif aleatorio de la carpeta 'casamiento'
            await ctx.send(f"{ctx.author.mention} y {member.mention} se han casado ¡Felicidades!", file=discord.File(os.path.join('casamiento', random.choice(os.listdir('casamiento')))))
        else:
            await ctx.send(f"{member.mention} ha rechazado tu propuesta de matrimonio. ¡Sigue intentando!")

@bot.command(help='Divorciarse de alguien con quien ya estes casado')
async def divorciar(ctx, member: discord.Member):
    author = ctx.message.author
    guild = ctx.guild
    
    # Buscar los roles "casad@" con el nombre del autor y del usuario mencionado
    author_role = discord.utils.get(guild.roles, name=f"casad@ con {member.name}")
    member_role = discord.utils.get(guild.roles, name=f"casad@ con {author.name}")
    
    # Comprobar si el usuario mencionado tiene el rol "casad@"
    if member_role not in member.roles:
        await ctx.send(f"{member.mention} no está casad@, no se puede divorciar.")
        return
    
    # Comprobar si el autor tiene el rol "casad@"
    if author_role not in author.roles:
        await ctx.send(f"{author.mention} no está casad@, no se puede divorciar.")
        return
    
    # Quitar los roles "casad@" con los nombres correspondientes al autor y al usuario mencionado
    await member.remove_roles(member_role)
    await author.remove_roles(author_role)
    
    # Enviar un mensaje de confirmación
    await ctx.send(f"{author.mention} y {member.mention} se han divorciado.")

@bot.command(help='Muestra el avatar de un usuario mencionado, o del autor')
async def avatar(ctx, user: discord.Member = None):
    user = user or ctx.author  # Si no se proporciona un usuario, se utiliza el usuario que emitió el comando
    embed = discord.Embed(title=f"Avatar de {user.name}", color=0x60f4f4)
    embed.set_image(url=user.avatar)  # Obtener la URL del avatar del usuario y configurarla en la imagen del embed
    await ctx.send(embed=embed)

@bot.command(help='Efecto arcoiris durante 14s')
@commands.cooldown(1, 585.71, commands.BucketType.user)
async def fiesta(ctx):
    role = discord.utils.get(ctx.guild.roles, name='fiesta')
    if role is None:
        await ctx.send("Se requiere un rol llamado 'fiesta' para usar este comando. Por favor, asegúrate de que haya un rol llamado 'fiesta' ubicado encima del rol del usuario.")
        return

    stop = False

    # Asignar el rol al usuario
    await ctx.author.add_roles(role)
    await ctx.send(f"¡{ctx.author.mention} tiene el rol fiesta ahora!")

    # Cambiar el color del rol a arcoiris durante 14.29 segundos
    hue = random.random() # Valor aleatorio inicial de tono
    saturation = 1
    value = 1
    current_color = None

    for i in range(100):
        if stop:
            break
        hue += 0.05 # Aumentar el valor de tono
        hue = hue % 1 # Mantener el valor de tono dentro del rango [0, 1]
        current_color = discord.Color.from_hsv(hue, saturation, value)
        await role.edit(color=current_color)
        await asyncio.sleep(0.143) # disminuir el tiempo de sleep a 0.143 segundos

    # Quitar el rol al usuario después de cambiar el color del rol
    await ctx.author.remove_roles(role)
    await ctx.send(f"¡{ctx.author.mention} ya no tiene el rol fiesta! "
                   f"Podrás usar el comando nuevamente en {ctx.command.get_cooldown_retry_after(ctx) / 60:.0f} minutos.")

@fiesta.error
async def fiesta_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"No puedes usar este comando de nuevo aún. Intenta de nuevo en {ctx.command.get_cooldown_retry_after(ctx) / 60:.0f} minutos.")
    else:
        raise error

@bot.command(help='Muestra un mapa aleatorio de Valorant (excepto The Range)')
async def mapa(ctx):
    response = requests.get('https://valorant-api.com/v1/maps')
    maps = response.json()['data']
    
    # Filtrar la lista de mapas para excluir "The Range"
    filtered_maps = [m for m in maps if m['displayName'] != 'The Range']
    
    random_map = random.choice(filtered_maps)

    embed = discord.Embed(title=random_map['displayName'], color=0x60f4f4)
    embed.set_image(url=random_map['splash'])
    await ctx.send(embed=embed)

@bot.command(help='Muestra un arma aleatoria de Valorant')
async def arma(ctx):
    response = requests.get('https://valorant-api.com/v1/weapons')
    weapons = response.json()['data']

    random_weapon = random.choice(weapons)

    embed = discord.Embed(title=random_weapon['displayName'], color=0x60f4f4)
    embed.add_field(name="Precio", value=f"${random_weapon['shopData']['cost']}", inline=False)
    embed.add_field(name="Cadencia de fuego", value=f"{random_weapon['weaponStats']['fireRate']}", inline=False)
    embed.add_field(name="Daño de cabeza", value=f"{random_weapon['weaponStats']['damageRanges'][0]['headDamage']}", inline=False)
    embed.add_field(name="Daño de cuerpo", value=f"{random_weapon['weaponStats']['damageRanges'][0]['bodyDamage']}", inline=False)
    embed.add_field(name="Daño de piernas", value=f"{random_weapon['weaponStats']['damageRanges'][0]['legDamage']}", inline=False)
    embed.set_image(url=random_weapon['displayIcon'])

    await ctx.send(embed=embed)

@bot.command(help='Muestra un agente aleatorio de Valorant')
async def agente(ctx):
    response = requests.get('https://valorant-api.com/v1/agents?language=es-ES')
    agents = response.json()['data']
    
    random_agent = random.choice(agents)

    embed = discord.Embed(title=random_agent['displayName'], description=random_agent['description'], color=0x60f4f4)
    embed.set_image(url=random_agent['displayIcon'])
    await ctx.send(embed=embed)



@bot.command(help='Crea un nuevo rol con el nombre introducido y te lo asigna, si ya ha sido creado simplemente se asigna')
async def rol(ctx, nombre_rol):
    guild = ctx.guild
    try:
        # Verificar si el rol ya existe
        rol_existente = discord.utils.get(guild.roles, name=nombre_rol)

        # Si existe, asignarlo al usuario
        if rol_existente:
            await ctx.author.add_roles(rol_existente)
            embed = discord.Embed(title="Rol asignado correctamente", description=f"Se te ha asignado el rol '{nombre_rol}'.", color=0x60f4f4)
            await ctx.send(embed=embed)
        else:
            # Si no existe, crearlo y asignarlo al usuario
            nuevo_rol = await guild.create_role(name=nombre_rol, reason="Nuevo rol creado por el usuario")
            await nuevo_rol.edit(colour=discord.Color(0))
            await ctx.author.add_roles(nuevo_rol)

            embed = discord.Embed(title="Rol creado y asignado correctamente", description=f"Se ha creado el rol '{nombre_rol}' y se te ha asignado de forma exitosa.", color=0x60f4f4)
            await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(title="Error", description="No tengo permisos suficientes para crear o asignar un nuevo rol.", color=discord.Color.red())
        await ctx.send(embed=embed)
    except discord.HTTPException:
        embed = discord.Embed(title="Error", description="No se ha podido crear o asignar el rol. Por favor, comprueba que el nombre sea válido.", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(help='Elimina un rol existente con el nombre introducido')
async def norol(ctx, nombre_rol):
    guild = ctx.guild
    try:
        # Verificar si el rol existe
        rol_existente = discord.utils.get(guild.roles, name=nombre_rol)

        # Si existe, quitarlo al usuario
        if rol_existente:
            await ctx.author.remove_roles(rol_existente)
            embed = discord.Embed(title="Rol quitado correctamente", description=f"Se te ha quitado el rol '{nombre_rol}' de forma exitosa.", color=0x60f4f4)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description=f"No se ha encontrado el rol '{nombre_rol}'.", color=discord.Color.red())
            await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(title="Error", description="No tengo permisos suficientes para quitar un rol.", color=discord.Color.red())
        await ctx.send(embed=embed)
    except discord.HTTPException:
        embed = discord.Embed(title="Error", description="No se ha podido quitar el rol. Por favor, comprueba que el nombre sea válido.", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(help="Envia un MichiGif")
async def michi(ctx):
    michi_folder = "./michi"
    michi_files = os.listdir(michi_folder)
    michi_file = random.choice(michi_files)
    michi_path = os.path.join(michi_folder, michi_file)
    with open(michi_path, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@bot.command(help="Envia un Gif llorando")
async def llorar(ctx):
    llorar_folder = "./llorar"
    llorar_files = os.listdir(llorar_folder)
    llorar_file = random.choice(llorar_files)
    llorar_path = os.path.join(llorar_folder, llorar_file)
    with open(llorar_path, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@bot.command(help="Abrazar a alguien")
async def abrazar(ctx, member: discord.Member = None):

    # Obtener el usuario que ejecutó el comando
    author = ctx.author
    # Obtener el usuario mencionado en el mensaje
    mentioned_users = ctx.message.mentions
    # Verificar si el bot fue mencionado
    if bot.user in mentioned_users:
        # Enviar mensaje de advertencia al usuario que mencionó al bot
        message = f"A mí no me toques los cojones, {author.mention}, o te baneo crack."
        await ctx.send(message)
    else:
        # Si no se menciona a ningún usuario o se menciona a sí mismo
        if member is None or member.id == author.id:
            auto_folder = "./autoabrazar"
            autogifs = os.listdir(auto_folder)
            randomautogif = random.choice(autogifs)
            # Enviar mensaje de abrazo a sí mismo y el gif aleatorio
            message = f"{author.mention} se ha abrazado a sí mism@, qué triste."
            try:
                await ctx.send(message, file=discord.File(f"{auto_folder}/{randomautogif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")
        else:
            # Enviar mensaje de abrazo a otro usuario y el gif aleatorio
            # Obtener la carpeta de gifs
            gifs_folder = "./abrazar"
            # Obtener la lista de gifs
            gifs = os.listdir(gifs_folder)
            # Seleccionar un gif aleatorio
            randomgif = random.choice(gifs)           
            message = f"{author.mention} te está abrazando {member.mention}"
            try:
                await ctx.send(message, file=discord.File(f"{gifs_folder}/{randomgif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")

@bot.command(help="Saludar a alguien")
async def saludar(ctx, member: discord.Member = None):
    author = ctx.author
    # Obtener el usuario mencionado en el mensaje
    mentioned_users = ctx.message.mentions
    # Verificar si el bot fue mencionado
    if bot.user in mentioned_users:
        # Enviar mensaje de advertencia al usuario que mencionó al bot
        message = f"A mí no me toques los cojones, {author.mention}, o te baneo crack."
        await ctx.send(message)
    else:
        # Si no se menciona a ningún usuario o se menciona a sí mismo
        if member is None or member.id == author.id:
            auto_folder = "./autosaludar"
            autogifs = os.listdir(auto_folder)
            randomautogif = random.choice(autogifs)
            # Enviar mensaje de abrazo a sí mismo y el gif aleatorio
            message = f"{author.mention} se ha saludado a sí mism@, qué triste."
            try:
                await ctx.send(message, file=discord.File(f"{auto_folder}/{randomautogif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")
        else:
            # Enviar mensaje de abrazo a otro usuario y el gif aleatorio
            # Obtener la carpeta de gifs
            gifs_folder = "./saludar"
            # Obtener la lista de gifs
            gifs = os.listdir(gifs_folder)
            # Seleccionar un gif aleatorio
            randomgif = random.choice(gifs)           
            message = f"{author.mention} te está saludando {member.mention}"
            try:
                await ctx.send(message, file=discord.File(f"{gifs_folder}/{randomgif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")



@bot.command(help="besar a alguien")
async def besar(ctx, member: discord.Member = None):
    author = ctx.author
    # Obtener el usuario mencionado en el mensaje
    mentioned_users = ctx.message.mentions
    # Verificar si el bot fue mencionado
    if bot.user in mentioned_users:
        # Enviar mensaje de advertencia al usuario que mencionó al bot
        message = f"A mí no me toques los cojones, {author.mention}, o te baneo crack."
        await ctx.send(message)
    else:
        # Si no se menciona a ningún usuario o se menciona a sí mismo
        if member is None or member.id == author.id:
            auto_folder = "./autobesar"
            autogifs = os.listdir(auto_folder)
            randomautogif = random.choice(autogifs)
            # Enviar mensaje de abrazo a sí mismo y el gif aleatorio
            message = f"{author.mention} se ha besado a si mismo, que triste."
            try:
                await ctx.send(message, file=discord.File(f"{auto_folder}/{randomautogif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")
        else:
            # Enviar mensaje de abrazo a otro usuario y el gif aleatorio
            # Obtener la carpeta de gifs
            gifs_folder = "./besar"
            # Obtener la lista de gifs
            gifs = os.listdir(gifs_folder)
            # Seleccionar un gif aleatorio
            randomgif = random.choice(gifs)           
            message = f"{author.mention} le ha comido la boca a {member.mention}"
            try:
                await ctx.send(message, file=discord.File(f"{gifs_folder}/{randomgif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")



@bot.command(help="pegarle a alguien")
async def pegar(ctx, member: discord.Member = None):
    author = ctx.author
    # Obtener el usuario mencionado en el mensaje
    mentioned_users = ctx.message.mentions
    # Verificar si el bot fue mencionado
    if bot.user in mentioned_users:
        # Enviar mensaje de advertencia al usuario que mencionó al bot
        message = f"A mí no me toques los cojones, {author.mention}, o te baneo crack."
        await ctx.send(message)
    else:
        # Si no se menciona a ningún usuario o se menciona a sí mismo
        if member is None or member.id == author.id:
            auto_folder = "./autopegar"
            autogifs = os.listdir(auto_folder)
            randomautogif = random.choice(autogifs)
            # Enviar mensaje de abrazo a sí mismo y el gif aleatorio
            message = f"{author.mention} se ha pegado a si mismo, masoca o gilipollas?"
            try:
                await ctx.send(message, file=discord.File(f"{auto_folder}/{randomautogif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")
        else:
            # Enviar mensaje de abrazo a otro usuario y el gif aleatorio
            # Obtener la carpeta de gifs
            gifs_folder = "./pegar"
            # Obtener la lista de gifs
            gifs = os.listdir(gifs_folder)
            # Seleccionar un gif aleatorio
            randomgif = random.choice(gifs)           
            message = f"{author.mention} le ha pegado a  {member.mention}"
            try:
                await ctx.send(message, file=discord.File(f"{gifs_folder}/{randomgif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")


@bot.command(help="dispararle a alguien")
async def disparar(ctx, member: discord.Member = None):
    author = ctx.author
    # Obtener el usuario mencionado en el mensaje
    mentioned_users = ctx.message.mentions
    # Verificar si el bot fue mencionado
    if bot.user in mentioned_users:
        # Enviar mensaje de advertencia al usuario que mencionó al bot
        message = f"A mí no me toques los cojones, {author.mention}, o te baneo crack."
        await ctx.send(message)
    else:
        # Si no se menciona a ningún usuario o se menciona a sí mismo
        if member is None or member.id == author.id:
            auto_folder = "./autodisparar"
            autogifs = os.listdir(auto_folder)
            randomautogif = random.choice(autogifs)
            # Enviar mensaje de abrazo a sí mismo y el gif aleatorio
            message = f"{author.mention} se ha disparado a si mismo, RIP"
            try:
                await ctx.send(message, file=discord.File(f"{auto_folder}/{randomautogif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")
        else:
            # Enviar mensaje de abrazo a otro usuario y el gif aleatorio
            # Obtener la carpeta de gifs
            gifs_folder = "./disparar"
            # Obtener la lista de gifs
            gifs = os.listdir(gifs_folder)
            # Seleccionar un gif aleatorio
            randomgif = random.choice(gifs)           
            message = f"{author.mention} le ha metido unos balazos a  {member.mention}"
            try:
                await ctx.send(message, file=discord.File(f"{gifs_folder}/{randomgif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")

@bot.command(help="secuestrar a alguien")
async def secuestrar(ctx, member: discord.Member = None):
    author = ctx.author
    # Obtener el usuario mencionado en el mensaje
    mentioned_users = ctx.message.mentions
    # Verificar si el bot fue mencionado
    if bot.user in mentioned_users:
        # Enviar mensaje de advertencia al usuario que mencionó al bot
        message = f"A mí no me toques los cojones, {author.mention}, o te baneo crack."
        await ctx.send(message)
    else:
        # Si no se menciona a ningún usuario o se menciona a sí mismo
        if member is None or member.id == author.id:
            auto_folder = "./autosecuestrar"
            autogifs = os.listdir(auto_folder)
            randomautogif = random.choice(autogifs)
            # Enviar mensaje de abrazo a sí mismo y el gif aleatorio
            message = f"{author.mention} te has secuestrado a ti mismo, bobo o que?"
            try:
                await ctx.send(message, file=discord.File(f"{auto_folder}/{randomautogif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")
        else:
            # Enviar mensaje de abrazo a otro usuario y el gif aleatorio
            # Obtener la carpeta de gifs
            gifs_folder = "./secuestrar"
            # Obtener la lista de gifs
            gifs = os.listdir(gifs_folder)
            # Seleccionar un gif aleatorio
            randomgif = random.choice(gifs)           
            message = f"{author.mention} ha secuestrado a  {member.mention}, no creo que paguen rescate"
            try:
                await ctx.send(message, file=discord.File(f"{gifs_folder}/{randomgif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")

@bot.command(help="morder a alguien")
async def morder(ctx, member: discord.Member = None):
    author = ctx.author
    # Obtener el usuario mencionado en el mensaje
    mentioned_users = ctx.message.mentions
    # Verificar si el bot fue mencionado
    if bot.user in mentioned_users:
        # Enviar mensaje de advertencia al usuario que mencionó al bot
        message = f"A mí no me toques los cojones, {author.mention}, o te baneo crack."
        await ctx.send(message)
    else:
        # Si no se menciona a ningún usuario o se menciona a sí mismo
        if member is None or member.id == author.id:
            auto_folder = "./automorder"
            autogifs = os.listdir(auto_folder)
            randomautogif = random.choice(autogifs)
            # Enviar mensaje de abrazo a sí mismo y el gif aleatorio
            message = f"{author.mention} te has mordido a ti mismo, prefiero no opinar nada al respecto"
            try:
                await ctx.send(message, file=discord.File(f"{auto_folder}/{randomautogif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")
        else:
            # Enviar mensaje de abrazo a otro usuario y el gif aleatorio
            # Obtener la carpeta de gifs
            gifs_folder = "./morder"
            # Obtener la lista de gifs
            gifs = os.listdir(gifs_folder)
            # Seleccionar un gif aleatorio
            randomgif = random.choice(gifs)           
            message = f"{author.mention} le ha pegao un bocao a  {member.mention}"
            try:
                await ctx.send(message, file=discord.File(f"{gifs_folder}/{randomgif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")

@bot.command(help="Rescatar a alguien secuestrado")
async def rescatar(ctx, member: discord.Member = None):
    author = ctx.author
    # Obtener el usuario mencionado en el mensaje
    mentioned_users = ctx.message.mentions
    # Verificar si el bot fue mencionado
    if bot.user in mentioned_users:
        # Enviar mensaje de advertencia al usuario que mencionó al bot
        message = f"A mí no me toques los cojones, {author.mention}, o te baneo crack."
        await ctx.send(message)
    else:
        # Si no se menciona a ningún usuario o se menciona a sí mismo
        if member is None or member.id == author.id:
            auto_folder = "./autorescatar"
            autogifs = os.listdir(auto_folder)
            randomautogif = random.choice(autogifs)
            # Enviar mensaje de abrazo a sí mismo y el gif aleatorio
            message = f"{author.mention} se ha rescatado a si mismo, un@ crack vamos"
            try:
                await ctx.send(message, file=discord.File(f"{auto_folder}/{randomautogif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")
        else:
            # Enviar mensaje de abrazo a otro usuario y el gif aleatorio
            # Obtener la carpeta de gifs
            gifs_folder = "./rescatar"
            # Obtener la lista de gifs
            gifs = os.listdir(gifs_folder)
            # Seleccionar un gif aleatorio
            randomgif = random.choice(gifs)           
            message = f"{author.mention} ha rescatado a  {member.mention}"
            try:
                await ctx.send(message, file=discord.File(f"{gifs_folder}/{randomgif}"))
            except Exception as e:
                await ctx.send(f"No se pudo enviar el gif, intentalo de nuevo")

API_KEY = ''
@bot.command(help="Recomienda una peli aleatoria")
async def peli(ctx):
    response = requests.get('https://api.themoviedb.org/3/movie/top_rated', 
                            params={'api_key': API_KEY})
    top_rated_movies = response.json()['results']
    good_movies = [movie for movie in top_rated_movies if movie['vote_average'] >= 5]
    random_movie = random.choice(good_movies)
    movie_id = random_movie['id']
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}', 
                            params={'api_key': API_KEY, 'language': 'es'})
    movie_info = response.json()
    title = movie_info['title']
    platforms_response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers', 
                                      params={'api_key': API_KEY, 'language': 'es'})
    if platforms_response.status_code == 200:
        platforms = platforms_response.json().get("results", {}).get("ES", {}).get("flatrate", [])
        if platforms:
            platforms_str = ", ".join([p["provider_name"] for p in platforms])
        else:
            platforms_str = "No se encontraron plataformas disponibles."
    else:
        platforms_str = "No se pudo obtener la información de plataformas."
    description = movie_info['overview']
    poster_path = movie_info['poster_path']
    poster_url = f'https://image.tmdb.org/t/p/original{poster_path}'
    
    embed = discord.Embed(title=title, description=description, color=0x60f4f4)
    embed.add_field(name='Plataformas', value=platforms_str)
    embed.set_image(url=poster_url)
    await ctx.send(embed=embed)

@bot.command(help='Recomienda una serie aleatoria')
async def serie(ctx):
    response = requests.get('https://api.themoviedb.org/3/discover/tv?api_key=&sort_by=vote_average.desc&vote_count.gte=1000&language=es')
    if response.status_code == 200:
        series = response.json()["results"]
        selected_series = [serie for serie in series if serie["poster_path"] is not None and serie["vote_average"] >= 5]
        if len(selected_series) > 0:
            selected_serie = selected_series[random.randint(0, len(selected_series)-1)]
            serie_title = selected_serie["name"]
            serie_overview = selected_serie["overview"]
            serie_year = selected_serie["first_air_date"][:4]
            poster_url = "https://image.tmdb.org/t/p/w500" + selected_serie["poster_path"]
            platforms_response = requests.get(f'https://api.themoviedb.org/3/tv/{selected_serie["id"]}/watch/providers?api_key=')
            if platforms_response.status_code == 200:
                platforms = platforms_response.json().get("results", {}).get("ES", {}).get("flatrate", [])
                if len(platforms) > 0:
                    platforms_str = ", ".join([p["provider_name"] for p in platforms])
                    embed = discord.Embed(title=serie_title + f' ({serie_year})', description=serie_overview, color=0x60f4f4)
                    embed.set_image(url=poster_url)
                    embed.add_field(name="Plataformas", value=platforms_str, inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Lo siento, no se encontraron plataformas de streaming para esta serie.")
            else:
                await ctx.send("Lo siento, no se pudo obtener información de plataformas de streaming.")
        else:
            await ctx.send("Lo siento, no se encontraron series que cumplan con los criterios especificados.")
    else:
        await ctx.send("Lo siento, no se pudo obtener información de series.")        

CLIENT_ID = ''
CLIENT_SECRET = ''
USERNAME = ''
SCOPE = 'playlist-read-private'
@bot.command(help="Muestra todas mis playlists de Spotify")
async def playlist(ctx):
    # Autenticación en la API de Spotify
    REDIRECT_URI = 'http://localhost:8000' 
    # Autenticación en la API de Spotify
    token = util.prompt_for_user_token(USERNAME, SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)

    # Obtener todas las playlists del usuario
    playlists = sp.user_playlists(user=USERNAME)

    # Crear el embed con la información de las playlists
    embed = discord.Embed(title="Mis playlists de Spotify 🎧", color=0x60f4f4)

    for playlist in playlists['items']:
        # Construir el enlace a la playlist
        playlist_url = playlist['external_urls']['spotify']
        # Construir el texto que incluye el nombre de la playlist y el enlace
        playlist_text = "[{name}]({url}) - {num_songs} canciones".format(
            name=playlist['name'], url=playlist_url, num_songs=playlist['tracks']['total'])
        # Agregar el texto como un campo en el embed
        embed.add_field(name='\u200b', value=playlist_text, inline=False)

    # Enviar el embed al canal de Discord
    await ctx.send(embed=embed)

PLAYLIST_ID = ''
@bot.command(help="Te recomienda una canción aleatoria de mi Spotify")
async def tema(ctx):
    # Autenticación en la API de Spotify
    REDIRECT_URI = 'http://localhost:8000'
    # Autenticación en la API de Spotify
    token = util.prompt_for_user_token(USERNAME, SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)

    # Obtener las canciones de la playlist
    results = sp.user_playlist_tracks(USERNAME, playlist_id=PLAYLIST_ID)
    tracks = results['items']

    # Seleccionar un tema aleatorio
    track = random.choice(tracks)['track']

    # Obtener los enlaces de la canción, artista y álbum
    song_link = track['external_urls']['spotify']
    artist_link = track['artists'][0]['external_urls']['spotify']
    album_link = track['album']['external_urls']['spotify']

    # Crear el embed con la información del tema
    embed = discord.Embed(title='🎶 Canción recomendada 🎶', color=0x60f4f4, description=f"**{track['name']}**")
    embed.set_author(name='Spotify', url='https://www.spotify.com/', icon_url='https://cdn-icons-png.flaticon.com/512/174/174872.png')
    embed.set_thumbnail(url=track['album']['images'][0]['url'])
    embed.add_field(name="Artista", value=f"[{track['artists'][0]['name']}]({artist_link})", inline=False)
    embed.add_field(name="Álbum", value=f"[{track['album']['name']}]({album_link})", inline=False)
    embed.add_field(name="Enlace", value=f"[Escuchar en Spotify]({song_link})", inline=False)

    # Enviar el embed al canal de Discord
    await ctx.send(embed=embed)

@bot.command(help='Dice cuanto tiempo queda para tu cumple, formato: dd/mm/aaaa')
async def cumple(ctx, fecha_nacimiento_str):
    formato_fecha = "%d/%m/%Y"
    fecha_actual = datetime.now()

    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, formato_fecha)
        fecha_cumple = fecha_nacimiento.replace(year=fecha_actual.year)
        if fecha_cumple < fecha_actual:
            fecha_cumple = fecha_cumple.replace(year=fecha_actual.year + 1)
    except ValueError:
        await ctx.send("La fecha proporcionada no está en el formato correcto.")
        return

    tiempo_faltante = fecha_cumple - fecha_actual
    dias_faltantes = tiempo_faltante.days
    horas_faltantes = tiempo_faltante.seconds // 3600
    minutos_faltantes = (tiempo_faltante.seconds // 60) % 60
    segundos_faltantes = tiempo_faltante.seconds % 60

    # Cálculo de la edad
    edad = fecha_actual.year - fecha_nacimiento.year
    if fecha_actual.month < fecha_nacimiento.month or (fecha_actual.month == fecha_nacimiento.month and fecha_actual.day < fecha_nacimiento.day):
        edad -= 1
    
    if dias_faltantes == 365:
        mensaje_respuesta = f"¡Hoy es tu cumpleaños! Felicidades por cumplir {edad} años."
    else:
        mensaje_respuesta = f"Faltan {dias_faltantes} días, {horas_faltantes} horas, {minutos_faltantes} minutos y {segundos_faltantes} segundos para tu cumpleaños. ¡Y cumplirás {edad+1} años!"

    embed = discord.Embed(title="Tiempo Restante para tu Cumpleaños", description=mensaje_respuesta, color=0x60f4f4)
    await ctx.send(embed=embed)

@bot.command(help='Muestra un link de invitacion')
async def invitar(ctx):
    embed = discord.Embed(color=0x60f4f4)
    embed.add_field(name="Invitación", value="[Haz clic aquí para invitar](https://discord.com/api/oauth2/authorize?client_id=1034498704415146035&permissions=8&scope=bot)")
    await ctx.send(embed=embed)

@bot.command(help='Responde con si, no, probablemente y porsupuesto que si de forma aleatoria')
async def al(ctx):
    responses = ["sí", "no", "probablemente", "por supuesto que sí"]
    response = random.choice(responses)
    
    embed = discord.Embed(color=0x60f4f4)
    embed.add_field(name="8ball", value=response)
    await ctx.send(embed=embed)

@bot.command(help='Al introducir un nombre te lo devuelve en un formato de letras gigantes permitidas en valorant')
async def riotid(ctx, *, text):
    japanese_text = ''
    conversions = [
        ('A', 'Ａ'), ('B', 'Ｂ'), ('C', 'Ｃ'),
        ('D', 'Ｄ'), ('E', 'Ｅ'), ('F', 'Ｆ'), ('G', 'Ｇ'), ('H', 'Ｈ'), ('I', 'Ｉ'), ('J', 'Ｊ'),
        ('K', 'Ｋ'), ('L', 'Ｌ'), ('M', 'Ｍ'), ('N', 'Ｎ'), ('O', 'Ｏ'), ('P', 'Ｐ'), 
        ('Q', 'Ｑ'), ('R', 'Ｒ'), ('S', 'Ｓ'), ('T', 'Ｔ'),
        ('U', 'Ｕ'), ('V', 'Ｖ'), ('W', 'Ｗ'), ('X', 'Ｘ'), ('Y', 'Ｙ'), ('Z', 'Ｚ'),
        ('a', 'ａ'), ('b', 'ｂ'), ('c', 'ｃ'), ('d', 'ｄ'), ('e', 'ｅ'), ('f', 'ｆ'), ('g', 'ｇ'), ('h', 'ｈ'), ('i', 'ｉ'), ('j', 'ｊ'),
        ('k', 'ｋ'), ('l', 'ｌ'), ('m', 'ｍ'), ('n', 'ｎ'), ('o', 'ｏ'), ('p', 'ｐ'), ('q', 'ｑ'), ('r', 'ｒ'), ('s', 'ｓ'), ('t', 'ｔ'),
        ('u', 'ｕ'), ('v', 'ｖ'), ('w', 'ｗ'), ('x', 'ｘ'), ('y', 'ｙ'), ('z', 'ｚ')
    ]
    for char in text:
        for conversion in conversions:
            if char == conversion[0]:
                japanese_text += conversion[1]
                break
        else:
            japanese_text += char
    
    # Crea un objeto Embed
    idriot = Embed(title='Tu Riot ID',
                  description=japanese_text,
                  color=0x60f4f4)  # Color 

    # Agrega un campo con un mensaje adicional
    idriot.add_field(name='Comprobación de la interfaz',
                    value="Para comprobar que el texto no se salga de la interfaz y quede como la mierda, revisa que tenga una longitud igual o menor a este:\n\nＧｈｏｓｔｙ一三ＳＡＮ三\n\nSi es mayor saldrá de la interfaz, besitos master.")

    # Envía el mensaje embed
    await ctx.send(embed=idriot)



"""@bot.command()
async def tienda(ctx, riotid):
    # hacer una llamada a la API de Riot para obtener los datos de la tienda
    riot_id = riotid.replace("#", "%23") # Reemplazar el símbolo '#' por su equivalente en la URL
    url = f"https://pd.eu.a.pvp.net/store/v3/storefront/{riot_id}"
    headers = {"X-Riot-Token": ""} # Reemplazar "insertar_tu_token_aqui" con tu token personal de Riot Games
    response = requests.post(url, headers=headers)
    print(response.text)
    if response.status_code == 200:
        data = response.json()
        # crear un embed con la información de la tienda
        embed = discord.Embed(title="Tienda de Valorant", color=0xFF4654)
        for offer in data["SkinsPanelLayout"]["Offers"]:
            skin_name = offer["Sku"]["DisplayName"]["TranslationName"]
            skin_price = offer["FinalPrice"]
            embed.add_field(name=skin_name, value=f"{skin_price} VP", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("No se pudo encontrar la tienda para ese Riot ID.") """

"""@bot.command(help='Muestra un anime aleatorio')
async def anime(ctx):
    response = requests.get("https://api.jikan.moe/v4/random/anime")
    data = response.json()
    try:
        title = data["data"]["title"]
        synopsis = data["data"]["synopsis"]
        image_url = data["data"]["images"]["jpg"]["large_image_url"]
        score = data["data"]["score"]
        if score is not None and score >= 8:
            embed = discord.Embed(title=title, description=synopsis, color=0x60f4f4)
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Lo siento, no se encontró ningún anime en este momento, intentalo de nuevo")
    except KeyError:
        await ctx.send("Lo siento, no se encontró ningún anime en este momento, intentalo de nuevo.")"""

"""@bot.command(help="rango del usuario de riot")
async def rango(ctx, riotid):
    headers = {
        "X-Riot-Token": "API_KEY_HERE"
    }
    url = f"https://eu.api.riotgames.com/val/content/v1/contents"
    response = requests.get(url, headers=headers).json()

    # Obtener el ID del jugador
    url = f"https://eu.api.riotgames.com/val/match/v1/matchlists/by-puuid/{riotid}/?startIndex=0&endIndex=1"
    response = requests.get(url, headers=headers).json()

    # Si no se encuentra al jugador, mostrar un mensaje de error
    if not response["data"]:
        embed = discord.Embed(title="Error", description=f"No se encontró al usuario {riotid}", color=0xff0000)
        await ctx.send(embed=embed)
        return

    puuid = response["data"][0]["puuid"]

    # Obtener el rango del jugador
    url = f"https://eu.api.riotgames.com/val/ranked/v1/rankedtiers/by-uuid/{puuid}"
    response = requests.get(url, headers=headers).json()

    # Si el jugador no tiene rango, mostrar un mensaje de error
    if not response["tier"]:
        embed = discord.Embed(title="Error", description=f"El usuario {riotid} no tiene rango en el Acto actual.", color=0xff0000)
        await ctx.send(embed=embed)
        return

    # Crear el embed con la información del jugador
    rank_name = response["tier"]["name"]
    rank_division = response["tier"]["division"]
    rank_points = response["ratedRating"]
    pickrate = response["games"]["totalGamesPlayed"] / response["games"]["totalSessionsPlayed"]

    embed = discord.Embed(title=f"Rango de {riotid} en el Acto {act_id}", color=0x60f4f4)
    embed.add_field(name="Rango", value=f"{rank_name} {rank_division} ({rank_points} puntos)", inline=True)
    embed.add_field(name="Pickrate", value=f"{pickrate:.2%}", inline=True)
    await ctx.send(embed=embed)"""



"""ID_DEL_CANAL = 947128034392166501 # Reemplazar 123456789 con el ID del canal donde quieres enviar el mensaje

STREAMERS = ['ivanmp26', 'ailyn94'] # Agrega los nombres de usuario de Twitch de los streamers que deseas seguir


def get_streamer_status(streamer):
    url = f'https://api.twitch.tv/helix/streams?user_login={streamer}'
    headers = {'Client-ID': 'tu_client_id_de_twitch'} # Reemplazar "tu_client_id_de_twitch" con tu Client ID de Twitch
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data['data'][0]['type'] == 'live' if len(data['data']) > 0 else False

async def send_live_notification(streamer):
    channel = bot.get_channel(ID_DEL_CANAL)
    embed = discord.Embed(title="¡Estoy en directo en Twitch!", description="¡No te lo pierdas!", color=0x6441A4)
    embed.add_field(name="Juego", value="Overwatch", inline=True)
    embed.add_field(name="Canal de Twitch", value=f"[{streamer}](https://www.twitch.tv/{streamer})", inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/yHQUU7D.png")
    await channel.send(embed=embed)

async def check_streamers():
    while True:
        for streamer in STREAMERS:
            if get_streamer_status(streamer):
                await send_live_notification(streamer)
        await asyncio.sleep(30) # Esperar 10 minutos antes de volver a verificar los streamers"""

"""@bot.event
async def on_member_join(member):
    avatar_url = member.avatar
    member_name = member.name
    welcome_messages = ["Un mamawebo se ha unido", "Y este olor a otaku?", "+ 1 drogadcito en el servidor"]
    random_welcome_message = random.choice(welcome_messages)
    embed = discord.Embed(title=random_welcome_message, description=f"Bienvenido al servidor, {member_name}!", color=0x60f4f4)
    embed.set_thumbnail(url=avatar_url)
    channel = bot.get_channel(947128099332562995)
    await channel.send(embed=embed)"""
# Ejecutar el bot
bot.run(TOKEN)
