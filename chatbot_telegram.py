

#Angelina Santana
# 2-16-2012
# from argparse import Action
from cgitb import text
from socket import timeout
from tracemalloc import start
from turtle import update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, keyboardbutton, ReplyKeyboardMarkup
import pyodbc

documento,nombre,apellido,direccion,telefono,envio,id_persona, id_cli, idped_cli,cod_art,importe,precio,cantidad  = range(13)
# importe,precio,cantidad = 0,0,0

persona = []
pedidos = []
compras = []

def db_connect():
    host= 'FERNANDO'
    dtbase = 'chatbot'
    user = 'angelina'
    password = 'chatbot'

    return pyodbc.connect(DRIVER='{SQL Server}',host=host,DATABASE=dtbase, user = user, password=password)

def db_disconnect():
    conn = db_connect()
    cur = conn.cursor()
    
    cur.close()
    conn.close()


# def cmd_start(update, context):
#     ''' START '''
#     chat_id = update.message.chat_id
#     # Enviar un mensaje a un ID determinado.
#     bot_msg = "Bienvenido, Comandos disponibles:\n" \
#             "- /start\n" \
#             "- /bye\n" \
#             "- /productos\n"\
#             "- /recomendaciones\n"
#     context.bot.send_message(chat_id, bot_msg)

def cmd_bye(update, context):
    # Bye
    context.bot.send_message(update.message.chat_id, "Adios")

def cmd_articulos(update,context):
    "Consulta Articulos"
    conn = db_connect()
    cur = conn.cursor()

    query = 'select top 10 idart as Codigo, descart as Descripcion, prec_venta as Precio from articulos'
    cur.execute(query)
    # cur.commit()

    result = cur.fetchall()
    
    for row in result:
        print(row)	
        art ="Codigo: "+ str(row[0]) +"\nDescripcion:"+ str(row[1])+"\nPrecio:"+ str(row[2])
        update.message.reply_text(art)
    
    db_disconnect()

def cmd_recomendaciones(update, context):
    '''Botones de opciones para cuando el cliente desee una recomendaciones'''
    # chat_id = update.message.chat_id

    keyboard_list = [[ InlineKeyboardButton("Bicicletas de niños", callback_data=1)], 
        [InlineKeyboardButton("Bicicletas de confort", callback_data=2)],
        [InlineKeyboardButton("Bicicletas de cruceros", callback_data=3)],
        [InlineKeyboardButton("Bicicletas ciclocross", callback_data=4)],
        [InlineKeyboardButton("Bicicletas electricas", callback_data=5)],
        [InlineKeyboardButton("Bicicletas de montaña", callback_data=6)],
        [InlineKeyboardButton("Bicicletas de carretera", callback_data=7)],
        ]

    markup = InlineKeyboardMarkup(keyboard_list)
    update.message.reply_text("Por favor selecciona una categoria:",reply_markup=markup)


def callback_button_categoria(update, context):
    ''''Captura de la categoria y algoritmo para recomendaciones'''
    # chat_id = update.message.chat_id
    query = update.callback_query
    query.answer()

    idcategoria = query.data

    print(idcategoria)

    conn = db_connect()
    cur = conn.cursor()

    query = "select  top 10 art.idart as Codigo, art.descart as Descripcion, art.prec_venta as Precio, c.desc_categoria  as Categoria"\
    " from articulos as art inner join chatbot.dbo.categoria c "\
    " on art.id_categoria = c.id_categoria "\
    f" where c.id_categoria  = {idcategoria} "\
    " order by art.prec_venta desc"

    cur = conn.cursor()
    cur.execute(query)
    # cur.commit()

    result = cur.fetchall()

    for row in result:
        print(row)	
        art ="Codigo: "+str(row[0]) +"\nDescripcion:"+ str(row[1])+"\nPrecio:"+ str(row[2]) +"\nCategoria:"+str(row[3])
        update.callback_query.message.reply_text(art)
    
    db_disconnect()

# Funciones para las reservas y compras

def cmd_reservar(update, context):

    # chat = update.message.chat
    # chat.send_action(action=ChatAction.TYPING, timeout=None)    
    # chat_id = update.message.chat_id
    # context.bot.send_message(chat_id, "Por favor digita tu nombre")
    update.message.reply_text("Por favor digita tu Cedula")

    return documento

def cmd_comprar(update, context):

    # chat = update.message.chat
    # chat.send_action(action=ChatAction.TYPING, timeout=None)    
    # chat_id = update.message.chat_id
    # context.bot.send_message(chat_id, "Por favor digita tu nombre")
    update.message.reply_text("Por favor digita tu Cedula")

    return documento

def input_documento(update, context):
    text = update.message.text
    conn = db_connect()
    cur = conn.cursor()

    
    query2 = 'insert into documento(id_tip_doc, desc_doc) values(1,?)'
    cur.execute(query2,(text))
    cur.commit()

    # query = "select IDENT_CURRENT('documento') as IDENT_CURRENT"
    query = "SELECT MAX(id_doc) from documento"

    cur.execute(query)
    # cur.commit()
    
    result = cur.fetchall()

    for row in result:
        documento = row[0]
    
    persona.append(documento)
    print('Id documento: ',documento, 'Documento: ',text)

    
    db_disconnect()

    update.message.reply_text("Por favor digita tu nombre")

    return nombre

def input_nombre(update, context):
    nombre = update.message.text

    persona.append(nombre)
    # nombre = text
    print("El nombre es: ",nombre)

    update.message.reply_text("Por favor digita tu apellido")

    return apellido
    # if(text.lower()=="reservar"):
    #     chat = update.message.chat
    #     chat.send_action(action=ChatAction.TYPING, timeout=None)
    #     update.message.reply_text("input")
    # else:
    #     update.message.reply_text(str(text)+" hasta la proxima")
    #     return ConversationHandler.END

def input_apellido(update, context):
    apellido = update.message.text

    persona.append(apellido)
    print("El apellido es: ",apellido)

    update.message.reply_text("Por favor digita tu telefono")

    return telefono

def input_telefono(update, context):
    telefono = update.message.text

    persona.append(telefono)

    print("El telefono es: ",telefono)

    update.message.reply_text("Por favor digita tu Direccion")

    return direccion

def input_direccion(update, context):
    text = update.message.text
    
    conn = db_connect()
    cur = conn.cursor()
    
    query2 = "insert into direccion(nomdireccion)  values(?)"
    cur.execute(query2,(text))    
    cur.commit()
    # iddireccion|nomdireccion       |idsector
    # query = "select IDENT_CURRENT('direccion') as IDENT_CURRENT"
    query = "SELECT MAX(iddireccion)+1 from direccion"
    cur.execute(query)
    # cur.commit()

    result = cur.fetchall()

    for row in result:
        direccion = row[0] 

    persona.append(direccion)
    
    print('Id direccion: ',direccion, 'Direccion: ',text)
    print('Telefono: ', telefono)


    query3 = 'insert into persona(id_doc,nom_persona,ape_persona,telefono,iddireccion) '\
        ' values(?,?,?,?,?)'
    cur.execute(query3,(persona[0],persona[1],persona[2],persona[3],persona[4]))
    cur.commit()

    print("Documento: ",persona[0],"Nombre: ", persona[1],"Apellido: ", persona[2],"Telefono: ", persona[3],"Direccion: ", persona[4])
    # for row in persona:
    #     cur.execute

    # query4 = "select IDENT_CURRENT('persona') as IDENT_CURRENT"
    query4 = "SELECT MAX(idpersona) from persona"
    cur.execute(query4)
    # cur.commit()

    result = cur.fetchall()

    for row in result:
        id_persona = row[0]
    
    print('Id persona: ',id_persona)

    query5 = "insert into clientes(idpersona) values(?)"
    cur.execute(query5,(id_persona))
    cur.commit()

    query6 = "SELECT MAX(idcli) from clientes"
    cur.execute(query6)
    # cur.commit()

    result = cur.fetchall()

    for row in result:
        id_cli = row[0]

    persona.append(id_cli)    
    print('Id cliente: ',id_cli)


    db_disconnect()

    update.message.reply_text("Por favor digita el codigo del articulo")

    return cod_art

def input_cod_art(update, context):
    cod_art = update.message.text
    conn = db_connect()
    cur = conn.cursor()

    pedidos.append(cod_art)

    db_disconnect()

    update.message.reply_text("Por favor digita la cantidad")

    return cantidad

def input_cantidad_reservada(update, context):
    cantidad = update.message.text
    conn = db_connect()
    cur = conn.cursor()

    pedidos.append(cantidad)
    print('Id cliente: ',persona[5])

    # query = "select IDENT_CURRENT('documento') as IDENT_CURRENT"
    query = "insert into pedidos_clientes(idstatus, idcli) values(4,?)"
    cur.execute(query,(persona[5]))
    cur.commit()

    query2 = "SELECT max(idped_cli) from pedidos_clientes"
    cur.execute(query2)
    # cur.commit()
   
    result = cur.fetchall()

    for row in result:
        idped_cli = row[0]
    
    pedidos.append(idped_cli)

    query3 = "select prec_venta from articulos where idart = ?"
    cur.execute(query3,(pedidos[0]))
    # cur.commit()
    result = cur.fetchall()

    for row in result:
        precio = row[0]
    
    pedidos.append(precio)
    # print("Precio: ",precio)

    # print("Cantidad: ",cantidad)
    # print("Precio: ",precio)

    importe =  (float(cantidad) * float(precio))
    print("Importe: ",importe)

    pedidos.append(importe)

    query4 = 'insert into detalles_pedidos_clientes(idart,cant,idped_cli,precio_art,envio,importe)'\
              ' values(?,?,?,?,100,?)'
    cur.execute(query4,(pedidos[0],pedidos[1],pedidos[2],pedidos[3],pedidos[4]))
    cur.commit()

    db_disconnect()

    update.message.reply_text("Reservacion creada, su numero de orden es: "+str(pedidos[2]))

    ConversationHandler.END
    # return direccion


def input_cantidad_comprada(update, context):
    cantidad = update.message.text
    conn = db_connect()
    cur = conn.cursor()

    compras.append(cantidad)

    # idventas|fecha_ventas|id_cli|iduser|total|idstatus|descuento
    query = "insert into ventas(id_cli,idstatus) values(?,1)"
    cur.execute(query,(persona[5]))
    cur.commit()

    query2 = "SELECT max(idventas) from ventas"
    cur.execute(query2)
    # cur.commit()
   
    result = cur.fetchall()

    for row in result:
        idped_cli = row[0]
    
    compras.append(idped_cli)

    query3 = "select prec_venta from articulos where idart = ?"
    cur.execute(query3,(pedidos[0]))
    # cur.commit()
    result = cur.fetchall()

    for row in result:
        precio = row[0]
    
    compras.append(precio)
    # print("Precio: ",precio)

    # print("Cantidad: ",cantidad)
    # print("Precio: ",precio)

    importe =  (float(cantidad) * float(precio))
    print("Importe: ",importe)

    compras.append(importe)

    # idventas|idart|cantidad|prec_ventas|importe|envio
    query4 = 'insert into det_ventas(idventas,idart,cantidad,prec_ventas,importe,envio)'\
              ' values(?,?,?,?,?,100)'
    cur.execute(query4,(compras[1],pedidos[0],compras[0],compras[2],compras[3]))
    cur.commit()

    db_disconnect()

    update.message.reply_text("Sr/Sra ",persona[1],", su numero de orden es: ",compras[1]," y total a pagar: ",compras[2])

    ConversationHandler.END
    # return direccion

# Fin para las reservas y compras

def msg_nocmd(update,context):
    '''Manejador para todos aquellos mensajes que no son comandos'''

    chat_id = update.message.chat_id
    # Enviar un mensaje a un ID determinado.
    bot_msg = "Bienvenido, Comandos disponibles:\n" \
            "- /bye\n" \
            "- /productos\n"\
            "- /recomendaciones\n"\
            "- /comprar\n"\
            "- /reservar\n"\
            "- /cancelar"

    context.bot.send_message(chat_id, bot_msg)


def main():
    print('Iniciando Bot')
    TOKEN="5556378517:AAH9s2B1B8Cusr-ljo0xnBAyWy68eOIphDk"
    updater=Updater(TOKEN, use_context=True)
    dp=updater.dispatcher


    # Eventos que activarán nuestro bot.
    # dp.add_handler(CommandHandler('start',	cmd_start))
    dp.add_handler(CommandHandler('bye', cmd_bye))
    dp.add_handler(CommandHandler('productos', cmd_articulos))
    dp.add_handler(CommandHandler('recomendaciones', cmd_recomendaciones))

    dp.add_handler(CallbackQueryHandler(callback_button_categoria))

    # Conversacion para reservacion
    dp.add_handler(ConversationHandler(entry_points=[CommandHandler('reservar',cmd_reservar)],
        allow_reentry=True,
        states={
            documento:[MessageHandler(Filters.text,input_documento)],
            nombre:[MessageHandler(Filters.text,input_nombre)],
            apellido:[MessageHandler(Filters.text,input_apellido)],
            telefono:[MessageHandler(Filters.text,input_telefono)],
            direccion:[MessageHandler(Filters.text,input_direccion)],
            cod_art:[MessageHandler(Filters.text,input_cod_art)],
            cantidad:[MessageHandler(Filters.text,input_cantidad_reservada)]
        },
        fallbacks={}
    ))

    # Conversacion para compras
    dp.add_handler(ConversationHandler(entry_points=[CommandHandler('comprar',cmd_comprar)],
        allow_reentry=True,
        states={
            documento:[MessageHandler(Filters.text,input_documento)],
            nombre:[MessageHandler(Filters.text,input_nombre)],
            apellido:[MessageHandler(Filters.text,input_apellido)],
            telefono:[MessageHandler(Filters.text,input_telefono)],
            direccion:[MessageHandler(Filters.text,input_direccion)],
            cod_art:[MessageHandler(Filters.text,input_cod_art)],
            cantidad:[MessageHandler(Filters.text,input_cantidad_comprada)]
        },
        fallbacks={}
    ))


    dp.add_handler(MessageHandler(Filters.text | Filters.photo | Filters.audio | Filters.voice | \
        Filters.video | Filters.sticker | Filters.document | Filters.location | Filters.contact, \
        msg_nocmd))

    # Comienza el bot
    updater.start_polling()
    # updater.start_polling(clean=True)
    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()



if __name__ == '__main__':
    main()