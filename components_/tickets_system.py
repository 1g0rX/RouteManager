# the bus system

from . import utils, lines_management
import os

def load_reserves():
    """
        Loads existing reservation lines from a file.

        Output format:
            list[list[str]]: List where each element is a reservation: [id, date, time].
            Example: [['R001', '2025-10-25', '14:00'], ...]
"""
    os.makedirs("data", exist_ok=True) # create the folder, if it aready exists, ignores
    reserves = dict()
    try:
        with open("data/reserves.txt", 'a') as file:
            for text_line in file:
                if text_line: # load info from the file, format: id, data, seats[]
                    data = text_line.split(", ") # separator
                    for i in data:
                        if i == 0: # if it is 0, will create the dictionary
                            reserves[data[0]] = {'date': data[1], 'seats': []}
                        elif i == 1:
                            pass # as we have already added the date, we do not need this
                        else: #here we will add the seats to the list of the reserved seats
                            reserves[data[0]]['seats'].append(data[i])
    except Exception as e:
        print(f"Error loading file: {e}")
    return reserves

def save_reserves(reserves):
    """
        Saves the dictionary of reservation data to the file.

        The function serializes the dictionary into text lines, with one reservation 
        per line, using the ID as the key.

        File Output Format (per line):
            ID, date1, date2, ..., time1, time2, ...

        Args:
            reserves (dict): A dictionary where keys are unique reservation IDs (str) 
                            and values are dictionaries containing 'dates' (list of str) 
                            and 'times' (list of str).
            
            Example Input Structure:
                {'R001': {'dates': ['2025-10-25'], 'times': ['14:00', '16:00'], 'seats': [1, 2]}, ...}
"""
    os.makedirs("data", exist_ok=True) # create the folder, if it aready exists, ignores

    try:
        with open("data/reserves.txt", 'w') as file:
            for id_line, info in reserves.items():
                string_dates = ', '.join(info['dates'])
                string_times = ', '.join(info['times'])
                string_seats = ', '.join(info['seats'])
                file.write(f"{id_line}, {string_dates}, {string_times}, {string_seats}")

    except Exception as e:
        print(f"Error while writing on file: {e}")

def draw_seats():
    '''
        Draw the seat in the terminal
    '''
    # as all the buses have 20 seats, there is no need to do code to create a matrix

    seats = [["[1]", "[2]", "[4]", "[3]"], 
             ["[5]", "[6]", "[8]", "[7]"], 
             ["[9]", "[10]", "[12]", "[11]"],
             ["[13]", "[14]", "[16]", "[15]"], 
             ["[17]", "[18]", "[20]", "[19]"]]
    
    ###############################################################
    # this funcion will receive a list of the seats sold. add a logic to mark the seats
    ###############################################################
    

    print(seats)
       

def sell_tickets(lines):
    utils.header('SELL TICKETS TO A STATION')  
    reserves = load_reserves()
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
        utils.header("Select the date and time for your ticket")
        date = input("Input the date (DD/MM/YYYY): ")
        time = input("Input the time (HH:MM): ")
        draw_seats()
        seat = input("Which seat do you want: ")
    ###############################################################
    # Insert the logic of choosing the seat according to matrix
    ###############################################################
    ###############################################################
    # Insert the logic of marking a seat as sold
    ###############################################################
        
        if id_line not in reserves.keys():
            reserves[id_line] = {'dates': [date], 'times': [time], 'seats': [seat]}
        else:
            if date not in reserves[id_line]['dates']:
                reserves[id_line]['dates'].append(date)
            if time not in reserves[id_line]['times']:
                reserves[id_line]['times'].append(time)
            if seat not in reserves[id_line]['seats']:
                reserves[id_line]['seats'].append(seat)
        save_reserves(reserves)
        print('Ticket sold successfully')
    ###############################################################
    # Insert the logic to check the date
    ###############################################################
 
def avaliable_seats(lines, reserves):
    """
        _Shows the available seats informing the city, date and time_
    """
    utils.header("VERIFY AVAILABLE SEATS")
    lines_management.list_lines(lines, 'no')
    destination = input("Input the destination city: ")
    date = input("Input the date (DD/MM/YYYY): ")
    time = input("Input the time (HH:MM): ")

    if destination not in lines.values():
        print("City not found!")
        utils.header("TICKET MENU - YOUR BEST TICKET MANAGER")
        return
    dates_list = list()
    for info in reserves.values():
        dates_list.append(info['dates'])
    if date not in dates_list:
        draw_seats()
    else:
        # verify if the time is any reserved, if it, send the seats to the draw_seats function
        pass



def tickets_menu():
    '''
        Shows the tickets meunu
    '''
    utils.header("TICKET MENU - YOUR BEST TICKET MANAGER")
    
    lines = lines_management.load_lines()

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
            
            case "2":
                pass

            case "3":
                pass

            case "0":
                break