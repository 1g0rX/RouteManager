# the bus system

from . import utils, lines_management
import os

def load_reserves():
    """
        Loads existing reservation lines from a file.

        Output format:
            dict{1{date, time, [seats]}}
            Example: {1: {'2025-10-25', '14:00', [7, 2, 4]}, ...}
    """
    os.makedirs("data", exist_ok=True) # create the folder, if it aready exists, ignores
    reserves = dict()
    try:
        with open("data/reserves.txt", 'r') as file:
            for text_line in file:
                text_line = text_line.strip()
                if text_line: # load info from the file, format: id, data, time, seats[]
                    parts = text_line.split(",") # separator
                    reserves[parts[0]] = {'date': parts[1], 'time': parts[2], 'seats': parts[3:]}
    except Exception as e:
        print(f"Error loading file: {e}")
    return reserves

def save_reserves(reserves):
    """
        Saves the dictionary of reservation data to the file.

        The function serializes the dictionary into text lines, with one reservation 
        per line, using the ID as the key.

        File Output Format (per line):
            ID, date, time, seat1, seat2, ...
    """
    os.makedirs("data", exist_ok=True) # create the folder, if it aready exists, ignores

    try:
        with open("data/reserves.txt", 'w') as file:
            for id_line, info in reserves.items():

                seats = ','.join(info['seats']) # transforms the list into a string

                file.write(f"{id_line},{info['date']},{info['time']},{seats}\n")

    except Exception as e:
        print(f"Error while writing on file: {e}")

def draw_seats(seats_list):
    '''
        Draw the seat in the terminal
    '''
    # as all the buses have 20 seats, there is no need to do code to create a matrix
    seats = list()
    seats_window = ['3', '7', '11', '15', '19']
    seats_hall = ['4', '8', '12', '16', '20']
    print(seats_list)
    
    # first, we'll build a list of seats
    for seat in range(1, 21):
        seats.append(seat)
    
    # now, we'll organize the seats, inverting the values to put the numbers in the window
    for seat in seats:
        if str(seat) in seats_window:
            seats[seat - 1] = seat + 1
        elif str(seat) in seats_hall:
            seats[seat - 1] = seat - 1

    # mark the sold tickets as 'X' and convert the list to str
    for i in range(len(seats)):
        seats[i] = str(seats[i])

    for i in range(len(seats)):
        if seats[i] in seats_list:
            seats[i] = 'X'

    # now, draw the matrix
    print('-' * 20)
    print("Window\tHall\t\tHall\tWindow")
    for i in range(0, len(seats), 4):
        print(f"[{seats[i]}]\t[{seats[i+1]}]\t\t[{seats[i+2]}]\t[{seats[i+3]}]")
    print('-' * 20)
       

def sell_tickets(lines):
    utils.header('SELL TICKETS TO A STATION')  
    reserves = load_reserves()

    seats_list = list()


    print("Available lines and prices:")
    lines_management.list_lines(lines, 'no')
    ###############################################################
    # Insert the logic to check the date
    ###############################################################
    utils.pause()
    id_line = input("Input the ID of the line you want to sell tickets to: ")
    if id_line not in lines.keys():
        print("Invalid option")
        utils.pause()
        utils.header('SELL TICKETS TO A STATION')
    else:

        #catch the list from the reserves
        if id_line in reserves.keys():
            seats_list = reserves[id_line]['seats']

        utils.header("Select the date and time for your ticket")
        date = input("Input the date (DD/MM/YYYY): ")
        time = input("Input the time (HH:MM): ")
        draw_seats(seats_list)
        seat = input("Which seat do you want: ")
    ###############################################################
    # Insert the logic of choosing the seat according to matrix
    ###############################################################
    ###############################################################
    # Insert the logic of marking a seat as sold
    ###############################################################
        
        if id_line not in reserves.keys():
            reserves[id_line] = {'date': date, 'time': time, 'seats': [seat]}
        else:
            reserves[id_line]['seats'].append(seat)
        save_reserves(reserves)
        print('Ticket sold successfully')
    ###############################################################
    # Insert the logic to check the date
    ###############################################################
 
def available_seats(lines, reserves):
    """
        _Shows the available seats informing the city, date and time_
    """
    utils.header("VERIFY AVAILABLE SEATS")
    lines_management.list_lines(lines, 'no')

    available_lines = dict()

    destination = input("Input the destination city: ")
    city_found = False
    for line_id, infos in lines.items():
        if destination == infos['Destination']:
            city_found = True
            break
    if not city_found:
        print("City not found!")
        utils.pause()
        utils.header("TICKET MENU - YOUR BEST TICKET MANAGER")
        return

    date = input("Input the date (DD/MM/YYYY): ")
    time_found = False
    date_found = False
    for line_id, infos in reserves.items():
        if date == infos['date']:
            date_found = True
            break
    if date_found: # if the date in reserves, check the time
        time = input("Input the time (HH:MM): ")
        for line_id, infos in reserves.items():
            if time == infos['time']:
                time_found = True
                break
        if time_found: # if true, search the id
            for id_line, info in lines.items():
                if destination == info['Destination']: 
                    available_lines[id_line] = lines[id_line]
    else: # if the date is not reserved, show a default bus
        time = input("Input the time (HH:MM): ")
        for id_line, info in lines.items():
            if destination == info['Destination']: 
                available_lines[id_line] = lines[id_line]

    # now, show the lines available:
    lines_management.list_lines(available_lines, 'yes')
    print('-' * utils.size_of_title_layer)

    ###############################################################
    # add the sell funtion here
    ###############################################################

    

def tickets_menu():
    '''
        Shows the tickets meunu
    '''
    utils.header("TICKET MENU - YOUR BEST TICKET MANAGER")
    
    lines = lines_management.load_lines()
    reserves = load_reserves()

    while True:
        print("1. Sell a ticket")
        print("2. See available lines and prices")
        print("3. Don't decided yet")
        print("0. Return to main menu")

        op = input("Insert a option: ")

        match op:
            case "1":
                utils.header('SELL A TICKET')  
                sell_tickets(lines)
                reserves = load_reserves()
            
            case "2":
                available_seats(lines, reserves)
                utils.header("TICKET MENU - YOUR BEST TICKET MANAGER")

            case "3":
                draw_seats(['7', '9'])

            case "0":
                break