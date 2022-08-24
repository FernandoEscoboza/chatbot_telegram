
from unittest import result
from telegram.ext import Updater, CommandHandler
import pyodbc

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

def start(update, context):
	''' START '''
	# Enviar un mensaje a un ID determinado.
	context.bot.send_message(update.message.chat_id, "Bienvenido")

def bye(update, context):
	# Bye
	context.bot.send_message(update.message.chat_id, "Adios")

# def articulos(update, context):
# 	"Consulta Articulos"
# 	result = query()

# 	for i in result:
# 		context.bot.send_message(update.message.chat_id, i)

def query():
	conn = db_connect()
	cur = conn.cursor()

	query = 'SELECT  * from articulos a inner join stock s ON a.idart = s.idart '
	cur.execute(query)
	result = cur.fetchall()


	for i in result:
		print(i)

	db_disconnect()
	
	return result
	
def main():
	print('Iniciando Bot')
	TOKEN="5556378517:AAH9s2B1B8Cusr-ljo0xnBAyWy68eOIphDk"
	updater=Updater(TOKEN, use_context=True)
	dp=updater.dispatcher

	# Eventos que activarán nuestro bot.
	dp.add_handler(CommandHandler('start',	start))
	dp.add_handler(CommandHandler('bye', bye))
	# dp.add_handler(CommandHandler('ver_productos', articulos))

	# Comienza el bot
	updater.start_polling()
	# Lo deja a la escucha. Evita que se detenga.
	updater.idle()

	# print(conn, 'Database conectado')
	query()


if __name__ == '__main__':
	main()