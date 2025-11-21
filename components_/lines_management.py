# here, we'll manage the lines of our application.

from . import utils
import os

def load_lines():
    '''
        Load all existing lines from a file and store them
    '''
    lines = dict()
    os.makedirs("data", exist_ok=True) # create the folder, if it aready exists, ignores
    # open the file to load data
    try:
        with open('data/lines.txt', 'r') as file:
            for text_line in file:
                if text_line:
                    data = text_line.split(',')
                    lines[data[0]] = {"Origin": data[1], "Destination": data[2],
                                      "Time": data[3], "Price": float(data[4])}
    except Exception as e:
        print(f"Error while reading file: {e}")
    return lines

def save_lines(lines):
    '''
        Save all existing lines to a file
    '''
    os.makedirs("data", exist_ok=True) # Create a folder, if exists, ignore

    # open a file
    try:
        with open('data/lines.txt', 'w') as file:
            for id, details in lines.items():
                file.write(f"{id}, {details['Origin']}, {details['Destination']}, {details['Time']}, {details['Price']}")
    except Exception as e:
        print(f"Could not open file: {e}") 

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
    id_line = input('Input a ID for the line: ')
    if id_line in lines.keys(): 
        print('ID already in use. Please choose another one')
        utils.pause()
        utils.header('MANAGE LINES')
        return
    
    origin = input("Input the origin's name: ")
    destination = input("Input the destination: ")
    time = input("Input time: (HH:MM) ")
    price = float(input("Input price: R$"))

    # save these infos into the lines dictionary nested
    lines[id_line] = {'Origin': origin, 'Destination': destination, 'Time': time, 'Price': price}
    save_lines(lines)
    print('Line created successfully')


def edit_line(lines):
    '''
        Edit a line by its name or ID
    '''
    utils.header("EDIT A EXISTING LINE")

    list_lines(lines, 'no') # List the IDs, origin cities and destination cities
    id_option = input('Input the id of the line you want to edit: ')
    if id_option not in lines.keys(): # check if ID exists and is valid (in dictionary)
        print('Invalid option')
        utils.pause()
        utils.header("EDIT A EXISTING LINE")
    
    else:
        utils.header("Edit an option or press enter to move to the next one")

        origin = input("Input the origin's name: ")
        if origin != '':
            lines[id_option]['Origin'] = origin

        destination = input("Input the destination: ")
        if destination != '':
            lines[id_option]['Destination'] = destination

        time = input("Input time: (HH:MM) ")
        if time != '':
            lines[id_option]['Time'] = time

        price = float(input("Input price: R$"))
        if not price:
         lines[id_option]['Price'] = price
            

def remove_line(lines):
    ''' 
        Removes a line from circulation
    '''
    utils.header("REMOVE A LINE FROM CIRCULATION")
    list_lines(lines, 'no')
    id_line = '-1'
    while id_line not in lines.keys():
        if id_line == 0:
            print("Operation canceled succesfully")
            return
        id_line = input('Insert a valid id or 0 for cancel: ')
    removed_line = lines.pop(id_line) # remove selected ID and infos about it (origin, destination)
    print(f"Line {removed_line} removed successfully")

def list_lines(lines, show_header):
    ''' 
        List the available lines
    '''
    if show_header == 'yes':
        utils.header("LIST OF AVAILABLE LINES")
    
    if is_empty(lines):
        print("There is no line in circulation, please register one firs")
        utils.pause()
    else:
        for line_id , infos in lines.items():
            print(f"ID: {line_id} | Origin: {infos['Origin']} | Destination: {infos['Destination']} | Time: {infos['Time']} | Price: {'Price'}")
    print('-' * utils.size_of_title_layer)

    

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
        print("4. List lines")
        print("0. Return to main menu")
    
        op = input("Insert a option: ")

        match op:
            case '1':
                create_line(lines) # call the function that creates lines and adds them into dictionary 
            
            case '2':
                edit_line(lines) # calls edit line with all existing infos in dict.
            
            case '3':
                remove_line(lines)
            
            case '4':
                list_lines(lines, 'yes')

            case '0':
                break
