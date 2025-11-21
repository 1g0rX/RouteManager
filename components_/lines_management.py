# here, we'll manage the lines of our application.

from . import utils

def load_lines():
    '''
        Load all existing lines from a file and store them
    '''
    #to do
    lines = dict()
    return lines

def save_lines(lines):
    '''
        Save all existing lines to a file
    '''
    # to do
    pass

def is_empty(lines):
    '''
        Verify if the lines is empty and returns
    '''
    if len(lines) == 0:
        return True
    else:
        return False

def create_line(lines):
    ''' 
        Create a line and add it to the lines file
    '''
    
    utils.clean_screen()
    utils.header('CREATE A NEW LINE')

    # Start asking the user the things
    id_line = int(input('Input a ID for the line: '))
    if id_line in lines: 
        print('ID already in use. Please choose another one')
        return
    
    origin = input("Input the origin's name: ")
    destination = input("Input the destination: ")
    time = input("Input time: (HH:MM) ")
    price = float(input("Input price: R$"))

    # save these infos into the lines dictionary nested
    lines[id] = {'Origin': origin, 'Destination': destination, 'Time': time, 'Price': price}
    save_lines(lines)
    print('Line created successfully')


def edit_line(lines):
    '''
        Edit a line by its name or ID
    '''

    utils.header("EDIT A EXISTING LINE")

    # List the IDs, origin cities and destination cities
    for id, infos in lines.items():
        print(id) # print ID and infos about it (origin, destination)
        print(infos['Origin']) # print origin city name
        print(infos['Destination']) # print destination city name
        print('-' * len(infos['Origin'])) # print '-' for each origin city name length times
        print('\n') # print an empty space between each ID and infos about it (origin, destination)

    id_option = int(input('Input the id of the line you want to edit: '))
    if id_option not in lines: # check if ID exists and is valid (in dictionary)
        print('Invalid option')
    
    

def remove_line(lines, id = -1):
    ''' 
        Removes a line from circulation
    '''

    utils.header("REMOVE A LINE FROM CIRCULATION")
    lines.remove(id) # remove selected ID and infos about it (origin, destination)
    print("Line removed successfully")

def list_lines(lines):
    ''' 
        List the available lines
    '''
    utils.header("LIST OF AVAILABLE LINES")
    
    if is_empty(lines):
        print("There is no line in circulation, please register one firs")
        utils.pause()
    else:
        for id_linha, info in lines.items(): # iterate over the lines and print IDs, origin cities and destination cities
            print("ID   | Origin | Destination | Time")
            print(f"{id_linha}, {info['origin']} | {info['destination']} | {info['time']} | {info["prince"]}")

def manage_lines():
    '''
        Main function to manage lines
    '''
    utils.header('MANAGE LINES') # call the header function to format it as a heading screen 
    lines = load_lines()
    while True:
        print("1. Create a new Line")
        print("2. Edit an existing line")
        print("3. Delete a line")
        print("0. Return to main menu")
    
        op = input("Insert a option: ")

        match op:
            case '1':
                create_line(lines) # call the function that creates lines and adds them into dictionary 
            
            case '2':
                edit_line(lines) # calls edit line with all existing infos in dict.
            
            case '3':
                remove_line

            case '0':
                break
