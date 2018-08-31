from telegram.ext import Updater,CommandHandler,CallbackQueryHandler,ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import files, drive

updater = Updater(token='643507808:AAEcfontlmriVw2Dc341-GEq15dWnXyBskg')
dispatcher = updater.dispatcher

def start(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="Selecione a Linguagem")
    listLanguages(bot,update)

def listLanguages(bot,update):
    try:
        keyboard = []
        files = _file.showProjectsLanguage()
        for i in range(0,len(files)):
            keyboard.append([InlineKeyboardButton(files[i], callback_data='step1_'+files[i])])
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose:', reply_markup=reply_markup)
    except Exception as e:
        print(e)

def listProjects(bot, update):
    try:
        keyboard = []
        files = _file.showProjects()
        for i in range(0,len(files)):
            keyboard.append([InlineKeyboardButton(files[i], callback_data='step2_'+files[i])])
        reply_markup = InlineKeyboardMarkup(keyboard)
        #update.message.reply_text('Please choose:', reply_markup=reply_markup)
        bot.send_message(chat_id=507188149,text='Please choose:', reply_markup=reply_markup)
    except Exception as e:
        print(e)



def languagesButton(bot, update):
    query = update.callback_query
    parseData = query.data.split('_')
    if 'step1' in parseData[0]:
        _file.changeProjectLanguage(parseData[1])
        #bot.send_message(chat_id=update.message.chat_id, text="Selecione o Projeto")
        bot.send_message(chat_id=507188149, text="Selecione o Projeto")
        listProjects(bot,update)
        bot.edit_message_text(text="Você selecionou: {}".format(parseData[1]),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
    if 'step2' in parseData[0]:
        #convert filename with _
        parseData = parseData[1:]
        filename = ''
        for string in parseData:
            filename += string + '_'
        filename = filename[:-1]
        bot.edit_message_text(text="Você selecionou: {}".format(filename),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        _file.compactProject(filename)
        #Nao esta vindo um retorno
        if _drive.uploadFile(filename + '.zip',_file.getMimeType(filename+'.zip')):
            bot.send_message(chat_id=507188149, text="Arquivo Enviado")




listLanguagesCommand = CommandHandler('language', listLanguages)
startCommand = CommandHandler('start', start)
listProjectsCommand = CommandHandler('projects', listProjects)
updater.dispatcher.add_handler(CallbackQueryHandler(languagesButton))
dispatcher.add_handler(listLanguagesCommand)
dispatcher.add_handler(listProjectsCommand)
dispatcher.add_handler(startCommand)

_file = files.Files()
_drive = drive.Drive()

try:
    updater.start_polling()
    updater.idle()
except KeyboardInterrupt:
    quit()