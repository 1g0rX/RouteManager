from . import utils, lines_management, tickets_system
from datetime import datetime
import os


def process_report_output(report_content, default_filename):
    """Ask user where to save or display the report."""
    
    report_header = report_content.split('\n')[0]
    utils.header(report_header)
    
    while True:
        print("\nSelect output option:")
        print("1. Show on screen")
        print(f"2. Save to file ({default_filename})")
        
        choice = input("Option (1 or 2): ")
        
        if choice == '1':
            print("\n" + report_content)
            utils.pause()
            break
        elif choice == '2':
            try:
                with open(default_filename, 'w') as f:
                    f.write(report_content)
                print(f"\nReport saved at: {os.path.abspath(default_filename)}")
                utils.pause()
                break
            except Exception as e:
                print(f"Error saving file: {e}")
                utils.pause()
                break
        else:
            print("Invalid option. Try again.")

def generate_revenue_report(lines, reserves):
    """Report: Total revenue per line for the current month."""
    
    report_lines = ["MONTHLY REVENUE REPORT"]
    
    # Get date once to avoid inconsistencies
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    
    report_lines.append(f"Report for: {current_month:02d}/{current_year}\n")
    
    total_system_revenue = 0
    
    report_lines.append(f"{'ID':<5} | {'Route':<30} | {'Revenue':>12}")
    report_lines.append("-" * 50)
    
    for line_id, info in lines.items():
        line_revenue = 0
        
        if line_id in reserves:
            for trip in reserves[line_id]:
                try:
                    trip_date = datetime.strptime(trip['date'], "%d/%m/%Y")
                    
                    if trip_date.month == current_month and trip_date.year == current_year:
                        seats_sold = len(trip['seats'])
                        
                        if 'Price' in info and isinstance(info['Price'], (int, float)):
                            revenue = seats_sold * info['Price']
                            line_revenue += revenue
                        
                except ValueError:
                    continue
        
        route_str = f"{info['Origin']} -> {info['Destination']}"
        report_lines.append(f"{line_id:<5} | {route_str:<30} | R$ {line_revenue:>10.2f}")
        
        total_system_revenue += line_revenue
        
    report_lines.append("-" * 50)
    report_lines.append(f"TOTAL SYSTEM REVENUE: R$ {total_system_revenue:.2f}")
    return "\n".join(report_lines)


def generate_occupancy_report(lines, reserves):
    """Report: Average occupancy per line for each weekday."""
    
    report_lines = []
    
    days_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    header_line = f"{'Line ID':<10} {'Origin -> Dest':<30}"
    for day in days_names:
        header_line += f"{day:<8}"
    report_lines.append(header_line)
    report_lines.append("=" * 100)
    
    for line_id, info in lines.items():
        
        # Stats per weekday
        weekly_stats = {i: {'sold': 0, 'trips': 0} for i in range(7)}
        
        if line_id in reserves:
            for trip in reserves[line_id]:
                try:
                    trip_date = datetime.strptime(trip['date'], "%d/%m/%Y")
                    weekday = trip_date.weekday()
                    
                    weekly_stats[weekday]['sold'] += len(trip['seats'])
                    weekly_stats[weekday]['trips'] += 1
                except ValueError:
                    continue

        route_str = f"{info['Origin']} -> {info['Destination']}"
        line_output = f"{line_id:<10} {route_str:<30}"
        daily_occupancy_strings = []
        
        for i in range(7):
            stats = weekly_stats[i]
            
            if stats['trips'] > 0:
                total_capacity = stats['trips'] * 20
                occupancy_pct = (stats['sold'] / total_capacity) * 100
                daily_occupancy_strings.append(f'{occupancy_pct:.2f}%'.ljust(8))
            else:
                daily_occupancy_strings.append('N/A'.ljust(8))
        
        report_lines.append(line_output + "".join(daily_occupancy_strings))
        
    report_lines.append("=" * 100)
    return "\n".join(report_lines)

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
            report_content = generate_revenue_report(lines, reserves)
            process_report_output(report_content, "revenue_report.txt")
        elif op == '2':
            report_content = generate_occupancy_report(lines, reserves)
            process_report_output(report_content, "occupancy_report.txt")
        elif op == '0':
            break
        else:
            print("Invalid option")
