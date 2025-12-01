from . import utils, lines_management, tickets_system
from datetime import datetime

def generate_revenue_report(lines, reserves):
    """
    Generates report: Total revenue collected in the current month for each line.
    """
    utils.header("MONTHLY REVENUE REPORT")
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    print(f"Report for: {current_month}/{current_year}\n")
    
    total_system_revenue = 0
    
    for line_id, info in lines.items():
        line_revenue = 0
        
        if line_id in reserves:
            for trip in reserves[line_id]:
                try:
                    trip_date = datetime.strptime(trip['date'], "%d/%m/%Y")
                    # check if trip is in current month and year
                    if trip_date.month == current_month and trip_date.year == current_year:
                        seats_sold = len(trip['seats'])
                        revenue = seats_sold * info['Price']
                        line_revenue += revenue
                except ValueError:
                    continue # to skip invalid dates
        
        print(f"ID: {line_id} | Route: {info['Origin']} -> {info['Destination']}")
        print(f"Revenue: R$ {line_revenue:.2f}")
        print("-" * 30)
        
        total_system_revenue += line_revenue
        
    print(f"\nTOTAL SYSTEM REVENUE: R$ {total_system_revenue:.2f}")
    utils.pause()

    #####################################################################################
    # In the function below, we're going to use a fstring formating that I'll write here
    # to not foget, it's about reservate space in the table, i didn't use it before, but
    # is very useful to align thing. ==> str(f"variable:<10{or some other number}")
    #####################################################################################

def generate_occupancy_report(lines, reserves):
    """
    Generates report: Average percentage occupancy for each line on each day of the week.
    Displays a matrix.
    """
    utils.header("WEEKLY OCCUPANCY MATRIX")
    
    # days of week (0=Monday, 6=Sunday)
    days_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    print(f"{'Line ID':<10} {'Origin -> Dest':<30}", end="")
    for day in days_names:
        print(f"{day:<8}", end="")
    print("\n" + "=" * 100)
    
    for line_id, info in lines.items():
        # Initialize stats for this line: {0: {'sold': 0, 'trips': 0}, 1: ...}
        weekly_stats = {i: {'sold': 0, 'trips': 0} for i in range(7)}
        
        if line_id in reserves:
            for trip in reserves[line_id]:
                try:
                    trip_date = datetime.strptime(trip['date'], "%d/%m/%Y")
                    weekday = trip_date.weekday() # 0-6
                    
                    weekly_stats[weekday]['sold'] += len(trip['seats'])
                    weekly_stats[weekday]['trips'] += 1
                except ValueError:
                    continue

        # Print Line Info
        route_str = f"{info['Origin']} -> {info['Destination']}"
        print(f"{line_id:<10} {route_str:<30}", end="")
        
        # Calculate and print stats per day
        for i in range(7):
            stats = weekly_stats[i]
            if stats['trips'] > 0:
                # Max capacity is 20 per trip
                total_capacity = stats['trips'] * 20
                occupancy_pct = (stats['sold'] / total_capacity) * 100
                print(f"{occupancy_pct:6.1f}% ", end="")
            else:
                print(f"{'N/A':<8}", end="")
        print()
        
    print("\n")
    utils.pause()

def reports_menu():
    lines = lines_management.load_lines()
    reserves = tickets_system.load_reserves()
    
    while True:
        utils.header("MANAGEMENT REPORTS")
        print("1. Revenue Report (Current Month)")
        print("2. Weekly Occupancy Matrix")
        print("0. Back to Main Menu")
        
        op = input("Select an option: ")
        
        if op == '1':
            generate_revenue_report(lines, reserves)
        elif op == '2':
            generate_occupancy_report(lines, reserves)
        elif op == '0':
            break
        else:
            print("Invalid option")