# Some useful functions

import os

def pause():
    ''' 
        Pause the program and wait for user input.
    '''

    input("Press Enter to continue...")


def clean_screen():
    '''
        Clean the terminal before showing the next screen
    '''
    os.system('clear') # execute the 'clear' command to clean the terminal. GNU/Linux only


def header(text):
    '''
        Receive a text and format it to a header like in the console
    '''
    clean_screen() #clean the screen every time that this function is called
    print('=' * 40)
    print(text.center(40))
    print('=' * 40)

