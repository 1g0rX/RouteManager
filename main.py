# Main file

import components_
while True:
    components_.utils.header('Route Manager - Your best Ticket Manager')
    print("1. Manage lines")
    print("2. Sell Tickets")
    print("3. Don't decided yet")
    print("0. Exit ")
    print("\n")

    op = input("Insert a option: ")

    match op:
        case '1':
            components_.utils.header('MANAGE LINES')
            components_.lines_management.manage_lines()
        
        case '2':
            components_.utils.header('SELL TICKETS')
            components_.tickets_system.tickets_menu()

        case '3':
            components_.utils.header('')
        
        case '0':
            print('Exiting...')
            break

