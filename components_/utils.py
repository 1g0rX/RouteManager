# Some useful functions

import os
import platform
size_of_title_layer = 90

def pause():
    ''' 
        Pause the program and wait for user input.
    '''

    input("Press Enter to continue...")


def clean_screen():
    """
    Clean the terminal before showing the next screen
    """
    
    # Get the S.O name
    os_name = platform.system()
    if os_name == "Windows":
    
        command = 'cls'
    elif os_name in ["Linux", "Darwin"]:

        command = 'clear'
    else:
        # For others operation systems
        print("Unknown Operational System")
        return 
        
    os.system(command)

def header(text):
    '''
        Receive a text and format it to a header like in the console
    '''
    clean_screen() #clean the screen every time that this function is called
    print('=' * size_of_title_layer)
    print(text.center(size_of_title_layer))
    print('=' * size_of_title_layer)

