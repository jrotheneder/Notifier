from notifier_bot import *

def main():

    # The bot's internal state is saved between restarts, allowing to preseve 
    # items saved by users 
    global persistence 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    persistence_filename = os.path.join(script_dir, "persistence.dat")
    persistence = PicklePersistence(filepath = persistence_filename)

    # The bot's token (see the telegram-bot documentation) is stored in 
    # a configuration file
    with open('config/bot_token.txt', 'r') as file:
        bot_token = file.read().replace('\n', '')

    # Users need to be whitelisted in order to access the bot's functions; 
    # this works by loading a list of telegram user handles from a textfile
    with open('config/allowed_users.txt', 'r') as file:
        allowed_users = [line.rstrip() for line in file]
    user_filter = filters.User(username = allowed_users)
    admin_user = allowed_users[0]

    # Create the application
    application = Application.builder().token(bot_token).persistence(persistence).build()

    job_queue = application.job_queue

    HelpHandler = CommandHandler('help', help)
    StartHandler = CommandHandler('start', help)
    MsgHandler = CommandHandler('msg', msg)
    addHandler = CommandHandler('add', add, user_filter, block=True)
    removeHandler = CommandHandler('remove', remove, block=True)
    listTrackedHandler = CommandHandler('list', list_tracked_items)
    infoHandler = CommandHandler('info', command_item_info)
    InfoHandler = CommandHandler('Info', command_item_info)
    EmptyHandler = CommandHandler('empty', empty)

    ExplUpdateHandler = CommandHandler('update', manual_update, block=True)
    StartRegUpdateHandler = CommandHandler('monitor', start_regular_update, block=True)
    StopRegUpdateHandler = CommandHandler('stop_monitor', stop_regular_update, block=True)

    BackupHandler = CommandHandler('backup', backup_to_json, user_filter)
    RestoreFromUrlHandler = CommandHandler('restore', restore_from_url,
                                           user_filter, block=True)
    RestoreFromFileHandler = MessageHandler(filters.Document.ALL & user_filter,
                                            restore_from_file, block=True)

    logHandler = CommandHandler('logs', send_logs)
    defaultHandler = MessageHandler(filters.TEXT & ~filters.COMMAND, default_item_info)

    shutdown_handler = CommandHandler('shutdown', shutdown,
                                      filters.User(username=admin_user))

    application.add_handler(HelpHandler)
    application.add_handler(StartHandler)
    application.add_handler(MsgHandler)
    application.add_handler(InfoHandler)
    application.add_handler(addHandler)
    application.add_handler(removeHandler)
    application.add_handler(listTrackedHandler)
    application.add_handler(infoHandler)
    application.add_handler(ExplUpdateHandler)
    application.add_handler(EmptyHandler)
    application.add_handler(StartRegUpdateHandler)
    application.add_handler(StopRegUpdateHandler)
    application.add_handler(BackupHandler)
    application.add_handler(RestoreFromUrlHandler)
    application.add_handler(RestoreFromFileHandler)
    application.add_handler(logHandler)
    application.add_handler(defaultHandler)
    application.add_handler(shutdown_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

    logging.info("Started bot " + str(datetime.now()))

if __name__ == "__main__":
    main()
