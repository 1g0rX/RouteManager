# the bus system

from . import utils, lines_management
import os
from datetime import datetime, timedelta

message = '' # to be used in some functions (I know that doing this is not a good practice)

# definition of the reserves file
reserves_file = "data/reserves.txt"
BATCH_FILE = "data/batch_reserves.txt"
ERROR_LOG_FILE = "data/reserves_errors.txt"

def load_reserves(file=reserves_file):
    """
        Loads existing reservation lines from a file.

        Output format:
            dict{ id_line: [ {'date': date, 'time': time, 'seats': [seat1, seat2]} ] }
            
            Example: 
            {
                '1': [
                    {'date': '12/12/2025', 'time': '12:30', 'seats': ['1', '2']},
                    {'date': '13/12/2025', 'time': '10:00', 'seats': ['5']}
                ]
            }
    """
    os.makedirs("data", exist_ok=True) 
    reserves = dict()
    
    if not os.path.exists(file):
        return reserves

    try:
        with open(file, 'r') as f:
            for text_line in f:
                text_line = text_line.strip()
                if text_line: 
                     # parts[0] = id, parts[1] = date, parts[2] = time, parts[3:] = seats
                    raw_parts = text_line.split(",")
                    # Clean all parts to ensure matching works correctly
                    for p in raw_parts:
                        parts = p.strip()
                    
                
                    id_line = parts[0]
                    
                    # Ensure we have date and time even if no seats
                    if len(parts) >= 3:
                        date = parts[1]
                        time = parts[2]
                        
                        # standard if/else structure as requested
                        if len(parts) > 3:
                            seats = parts[3:]
                        else:
                            seats = []
                        
                        entry = {
                            'date': date, 
                            'time': time,  
                            'seats': seats
                        }
                         
                        # if the line ID is not in the dictionary, create a list for it
                        if id_line not in reserves:
                            reserves[id_line] = []
                        
                        # add this specific trip to the list of trips for this line
                        reserves[id_line].append(entry)
                    
    except Exception as e:
        print(f"Error loading file: {e}")
    return reserves

def save_reserves(reserves, file=reserves_file):
    """
        Saves the dictionary of reservation data to the file.
        Iterates through the list of trips for each line.
    """
    os.makedirs("data", exist_ok=True)

    try:
        with open(file, 'w') as f:
            for id_line, trips_list in reserves.items():
                # trips_list is a list of dictionaries (each trip) id: [{trip1}, {trip2}...]
                for trip in trips_list:
                    seats = ','.join(trip['seats']) 
                    # if there are seats, add a comma before them, otherwise empty string
                    if seats:
                        seats_str = f",{seats}"  
                    else:
                        seats_str = "" 
                    f.write(f"{id_line},{trip['date']},{trip['time']}{seats_str}\n")

    except Exception as e:
        print(f"Error while writing on file: {e}")

def validate_date_time(date_str, time_str):
    """
    Validates if the date and time are valid for reservation.
    Returns (True) if valid, or (False) if invalid, and change the message global variable, (true or error cause if false).
    Rules:
    1. Date must be within the next 30 days.
    2. Bus cannot have already departed.
    """

    global message # to change, in the code, the global variable
    try:
        # combine date and time strings into a datetime object
        bus_datetime = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
        now = datetime.now()
        
        # check if the bus has already departed
        if bus_datetime < now:
            message = "The bus has already departed."
            print(f"Error: {message}")
            return False
    
        
        # check if the date is more than 30 days from now
        limit_date = now + timedelta(days=30)
        if bus_datetime > limit_date:
            message = "Reservations can only be made up to 30 days in advance."
            print(f"Error: {message}")
            return False
            
        message = 'Valid'
        return True
    
    except ValueError:
        message = "Invalid date or time format. Use DD/MM/YYYY and HH:MM."
        print(f"Error: {message}")
        return False


def log_error(reason, line_data):
    """
    Logs failed reservations to a text file.
    """
    try:
        with open(ERROR_LOG_FILE, 'a') as f:
            f.write(f"FAILED: {line_data} | REASON: {reason}\n")
    except Exception as e:
        print(f"Could not write to error log: {e}")

def batch_reservation(lines, reserves):
    """
    Process reservations from a batch file.
    Format: CITY, TIME, DATE, SEAT
    """
    utils.header("BATCH PROCESSING")
    
    if not os.path.exists(BATCH_FILE):
        print(f"Batch file '{BATCH_FILE}' not found.")
        print("Please create it with format: CITY,TIME,DATE,SEAT (one per line)")
        utils.pause()
        return

    processed_count = 0
    errors_count = 0

    print("Processing reservations...")
    
    try:
        with open(BATCH_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split(',')
                if len(parts) < 4:
                    log_error("Invalid format", line)
                    errors_count += 1
                    continue
                # remove the spaces to avoid ' string' and stay 'string'
                city = parts[0].strip()
                time = parts[1].strip()
                date = parts[2].strip()
                seat = parts[3].strip()
                
                # First, find Line ID based on City and Time
                found_id = None
                for line_id, info in lines.items():
                    # Check destination OR origin (as requested), and then check time
                    if (info['Destination'].lower() == city.lower() or info['Origin'].lower() == city.lower()) and info['Time'] == time:
                        found_id = line_id
                        break
                
                if not found_id:
                    log_error(f"No line found for {city} at {time}", line)
                    errors_count += 1
                    continue
                
                # Second, validate Date and Time rules
                is_valid = validate_date_time(date, time)
                if not is_valid:
                    log_error(message, line)
                    errors_count += 1
                    continue

                # third, check if the seat is available
                current_trip = None
                if found_id in reserves:
                    for trip in reserves[found_id]:
                        if trip['date'] == date and trip['time'] == time:
                            current_trip = trip
                            break
                
                if current_trip:
                    seats_taken = current_trip['seats']
                else:
                    seats_taken = []
                
                if len(seats_taken) >= 20:
                    log_error("Bus is full", line)
                    errors_count += 1
                    continue
                    
                if seat in seats_taken:
                    log_error(f"Seat {seat} occupied", line)
                    errors_count += 1
                    continue
                
                # Validation for seat number
                if not seat.isdigit() or int(seat) < 1 or int(seat) > 20:
                    log_error(f"Invalid seat number {seat}", line)
                    errors_count += 1
                    continue

                # Finally, success - Book it
                if current_trip:
                    current_trip['seats'].append(seat)
                else:
                    new_trip = {'date': date, 'time': time, 'seats': [seat]}
                    if found_id not in reserves:
                        reserves[found_id] = []
                    reserves[found_id].append(new_trip)
                
                processed_count += 1

        # Save changes (don't forget)
        save_reserves(reserves, reserves_file)
        print("\nBatch processing finished.")
        print(f"Successful reservations: {processed_count}")
        print(f"Failed reservations: {errors_count}")
        if errors_count > 0:
            print(f"Check '{ERROR_LOG_FILE}' for details.")
            
    except Exception as e:
        print(f"Critical error during batch processing: {e}")
    
    utils.pause()

def draw_seats(seats_list):
    '''
        Draw the seat in the terminal
    '''
    seats = list()
    seats_window = ['3', '7', '11', '15', '19']
    seats_hall = ['4', '8', '12', '16', '20']
    
    # build a list of seats numbers
    for seat in range(1, 21):
        seats.append(seat)
    
    # organize the seats for visual representation
    for seat in seats:
        if str(seat) in seats_window:
            seats[seat - 1] = seat + 1
        elif str(seat) in seats_hall:
            seats[seat - 1] = seat - 1

    # convert to string to allow replacement with 'X'
    display_seats = [str(s) for s in seats]

    # mark the sold tickets as 'X'
    for i in range(len(display_seats)):
        # Check if the currently displayed number is in the taken list
        if display_seats[i] in seats_list:
            display_seats[i] = 'X'

    # now, draw the matrix
    print('-' * 45)
    print("Window\tHall\t\tHall\tWindow")
    for i in range(0, len(display_seats), 4):
        print(f"[{display_seats[i]}]\t[{display_seats[i+1]}]\t\t[{display_seats[i+2]}]\t[{display_seats[i+3]}]")
    print('-' * 45)
       

def sell_tickets(lines):
    utils.header('SELL TICKETS TO A STATION')  
    reserves = load_reserves()

    print("Available lines and prices:")
    lines_management.list_lines(lines, 'no')
    
    id_line = input("Input the ID of the line you want to sell tickets to or type 0 to cancel: ")

    if id_line == '0':
            print("Operation canceled successfully")
            return
    
    if id_line not in lines.keys():
        print("Invalid option")
        utils.pause()
        return 

    utils.header("Select the date and time for your ticket")
    date = input("Input the date (DD/MM/YYYY): ")
    
    ###############################################################
    # Here, we have a question, the bus have only one or more
    # schedules? 
    # As we already have the id, we'll assume that each line has
    # only one fixed schedule, but we will still asking to confirm
    ###############################################################

    scheduled_time = lines[id_line]['Time']
    
    print(f"The scheduled time for this line is: {scheduled_time}")
    time = input("Confirm the time (HH:MM): ")
    
    while time != scheduled_time:
        print("Warning: The time entered does not match the line schedule.")
        time = input("Confirm the time (HH:MM): ")
    
    # validate date and time rules
    is_valid = validate_date_time(date, time)
    if not is_valid:
        utils.pause()
        return

    # find the specific trip (Line + Date + Time)
    current_trip = None
    if id_line in reserves:
        for trip in reserves[id_line]:
            if trip['date'] == date and trip['time'] == time:
                current_trip = trip
                break
    if current_trip:
        seats_list = current_trip['seats']  
    else:
        seats_list = []

    if len(seats_list) >= 20:
        print("All seats are already sold for this schedule!")
        utils.pause()
        return

    draw_seats(seats_list)
    seat = input("Which seat do you want: ")
    
    # validating the seats number (is numeric and it is between 1 and 20)
    if not seat.isdigit() or int(seat) < 1 or int(seat) > 20:
        print("Invalid seat number (1-20).")
        utils.pause()
        return

    while seat in seats_list:
        print(f"Seat {seat} is not available.")
        seat = input("Please choose another one: ")
        if not seat.isdigit() or int(seat) < 1 or int(seat) > 20:
             print("Invalid seat.")
             utils.pause()
             return
    

    if current_trip:
        current_trip['seats'].append(seat)
    else:
        new_trip = {'date': date, 'time': time, 'seats': [seat]}
        if id_line not in reserves:
            reserves[id_line] = []
        reserves[id_line].append(new_trip)

    save_reserves(reserves, reserves_file)
    print('Ticket sold successfully')
    utils.pause()
    utils.header("TICKET MENU - YOUR BEST TICKET MANAGER")

 
def available_seats(lines, reserves):
    """
        Shows the available seats informing the city, date and time
        and allows immediate reservation.
    """
    utils.header("VERIFY AVAILABLE SEATS")
    lines_management.list_lines(lines, 'no')

    destination = input("Input the destination city: ")
    
    # find matching lines for destination
    matching_line_ids = []
    for line_id, infos in lines.items():
        if destination.lower() == infos['Destination'].lower():
            matching_line_ids.append(line_id)
            
    if not matching_line_ids:
        print("City not found or no lines for this destination!")
        utils.pause()
        return

    date = input("Input the date (DD/MM/YYYY): ")
    time = input("Input the time (HH:MM): ")
    
    # here, since it's just checking availability, but good to warn if user tries to buy
    is_valid = validate_date_time(date, time)
    if not is_valid:
        print(f"Note: {message}")
    
    found_lines = []
    
    # check availability
    print(f"\n--- Results for {destination} on {date} at {time} ---")
    
    for id_line in matching_line_ids:
        # check if the schedule matches
        line_schedule_time = lines[id_line]['Time']
        
        if line_schedule_time == time:
            found_lines.append(id_line)
            print(f"\n> Line ID: {id_line} | Origin: {lines[id_line]['Origin']} | Price: R${lines[id_line]['Price']}")
            
            # check occupied seats
            seats_taken = []
            if id_line in reserves:
                for trip in reserves[id_line]:
                    if trip['date'] == date and trip['time'] == time:
                        seats_taken = trip['seats']
                        break
            
            print(f"  Occupancy: {len(seats_taken)}/20")
            draw_seats(seats_taken)
        
    if not found_lines:
        print(f"No bus found for this destination at {time}.")
        utils.pause()
        return

    # ask if user wants to reserve
    print("-" * utils.size_of_title_layer)
    buy = input("Do you want to reserve a seat in any of these buses? (Y/N): ").upper()
    
    if buy == 'Y':
        if not is_valid:
            print(f"Cannot proceed with reservation: {message}")
            utils.pause()
            return

        target_id = input("Input the ID of the desired Line (from the list above): ")
        
        if target_id not in found_lines:
            print("Invalid ID or not part of current search.")
            utils.pause()
            return
            
        seat_to_buy = input("Which seat do you want to reserve? ")
        
        # here we'll implement the logic to validate and save
        current_trip = None
        if target_id in reserves:
            for trip in reserves[target_id]:
                if trip['date'] == date and trip['time'] == time:
                    current_trip = trip
                    break
        if current_trip:
            taken_seats = current_trip['seats']  
        else:
            taken_seats = []
        
        if seat_to_buy in taken_seats:
            print(f"Error: Seat {seat_to_buy} is already occupied.")
        elif not seat_to_buy.isdigit() or int(seat_to_buy) < 1 or int(seat_to_buy) > 20:
             print("Error: Invalid seat number.")
        else:
            # now, save
            if current_trip:
                current_trip['seats'].append(seat_to_buy)
            else:
                new_trip = {'date': date, 'time': time, 'seats': [seat_to_buy]}
                if target_id not in reserves:
                    reserves[target_id] = []
                reserves[target_id].append(new_trip)
            
            save_reserves(reserves, reserves_file)
            print(f"Reservation confirmed! Seat {seat_to_buy} on line {target_id}.")
            
    utils.pause()
    

def tickets_menu():
    '''
        Shows the tickets menu
    '''
    utils.header("TICKET MENU - YOUR BEST TICKET MANAGER")
    
    lines = lines_management.load_lines()
    reserves = load_reserves(reserves_file)

    while True:
        print("1. Buy a ticket")
        print("2. See available seats")
        #-------------------------------------------
        print("3. Batch processing (from file)")
        print("0. Return to main menu")

        op = input("Insert a option: ")

        match op:
            case "1":
                sell_tickets(lines)
                reserves = load_reserves(reserves_file)
            
            case "2":
                available_seats(lines, reserves)
                utils.header("TICKET MENU - YOUR BEST TICKET MANAGER")
            
            case "3":
                batch_reservation(lines, reserves)
                utils.header("TICKET MENU - YOUR BEST TICKET MANAGER")

            case "0":
                break
            
            case _:
                print("Invalid Option")