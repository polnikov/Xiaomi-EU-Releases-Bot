class MESSAGE:
    KB_STOP = ('⛔', 'stop')


    class KB_MAIN:
        ADD_ROM = ('add ROM', 'add-rom')
        DEL_ROM = ('delete ROM', 'delete-rom')
        GET_DATA = ('get my ROMs', 'get-user-data')
        DEL_DATA = ('delete all my ROMs', 'delete-user-data')


    class DIALOGS:
        INPUT_ROM = "Please input new phone\'s model ROM"
        SORRY = 'Sorry, there are no firmware for your ROM\nTry another, please'
        ALREADY_FOLLOW = 'You are already following this ROM\nTry another, please'
        WRONG = 'Something went wrong 🤔, please try again later'

        HI = "Hi! I can help you keep track of new Xiaomi.EU MiUIv14 firmware for your phone\nPlease input your phone\'s model ROM"
        WELCOME = 'Welcome back! ✌'

        NO_ROMS = 'You have no saved ROMs 🤷'
        CHOOSE = 'Choose which rom to delete'

        ALL_REMOVED = 'All your ROMs was successful removed ✅'
