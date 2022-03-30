from loading_data import *
import classes
from classes import *

time_message = 'Please Enter Hours as 4-Digit Military Time: Ex. 0900'

# Layout Functions

"""
The functions in this section are simple functions used to display text for the gui.
"""


# Function contains title of project
def header():
    print(''.ljust(100, '*'))
    print('*' + '--Delivery Management Software--'.rjust(60, ' ') + "*".rjust(40 - 1, ' '))
    print(''.ljust(100, '*'))
    print("\n")

# Function Contains header text
def header_text():
    print('What do you want to check?')
    print("\n")
    print('Choice List:')
    print("")
    print('1. All Packages'.rjust(18, ' '))
    print('2. Package Number'.rjust(20, ' '))
    print('3. Total Mileage of Trucks'.rjust(29, ' '))
    print("\n")


# Function fills screen with characters
def pattern_fill(pattern, repetition, after):
    rep = repetition

    while rep > 0:
        print(pattern + pattern.rjust(after - 1, ' '))
        rep -= 1

def interface_text(hours1, hours2):
    print("\n")
    print('Package(s) Status Between the Hours of ' + str(hours1) + ' and ' + str(hours2) + ": ")
    print("\n")
    print("Package(s):")
    print("\n")
    print('{:10s} {:45.45s}    {:20.20s}     {:10s} {:10s} {}         {}'.format('ID:', 'Address:', 'City:','State:', 'Zip:', 'Status:', 'Delivered:'))
    print("")


# Interface Functions
"""
The function address_correct notifies the user of the package correction for package 9 depending on user time inputs.
"""


def address_correct(s_time, e_time):
    # If statement for when user enters inputs equal to or after the correction of package 9
    if s_time >= correction_time or e_time >= correction_time:

        print('*There was an address mistake on package number 9, and has been correct at 1020.')
        print("")

        address_display(9, package_hash, '410 S State St', 'Salt Lake City', 'UT', '84111',
                     'Address has been corrected')

    # If statement for when user enters inputs before the correction of package 9
    elif s_time < correction_time and e_time <correction_time:
        address_display(9, package_hash, '300 State St', 'Salt Lake City', 'UT', '84103',
                     'Wrong address listed')


"""
The function choice_repeat prompts users if they would like to select another option.
"""


def choice_repeat():
    again_answer = input("Select Choice Again?(Y/N): ")

    # When user inputs yes
    if again_answer.lower().strip() == 'y':
        print('')
        header_text()
        choice_prompt()
    # When user inputs no
    elif again_answer.lower().strip() == 'n':
        print("\n")
        print("Good Bye")
        print("")
    # When user inputs any inputs other than yes or no
    else:
        choice_repeat()


"""
The function all_status retrieves the status of packages between two points in time. 
"""


def all_truck_packages_status(hours1, hours2):
    # Calls function packages_status for all trucks
    print('Truck 1:')
    print("")
    status_of_packages(truck1, hours1, hours2)
    print("")
    print('Truck 2:')
    print("")
    status_of_packages(truck2, hours1, hours2)
    print("")
    print('Truck 3:')
    print("")
    status_of_packages(truck3, hours1, hours2)


"""
The function total_truck_mileage returns the total miles of all trucks from their delivery routes.
"""


def total_truck_mileage(truck1, truck2, truck3):
    answer = truck1.total_truck_mileage + truck2.total_truck_mileage + truck3.total_truck_mileage
    print('')
    print('Total Mileage: ' + str(round(answer, 2)))
    print('')


"""
The function choice_prompt prompts user to select an action for the information they are looking for. Users can find
statuses to all packages or an individual package and the total mileage of all trucks.
"""


def choice_prompt():
    choice = input("Please Enter Choice: ")

    # Checks if user input is numeric
    if choice.strip().isdigit():
        # If user inputs 1 for all package status
        if int(choice) == 1:
            print("")
            print(time_message)
            print("")

            try:
                time1 = input('Please Enter Start Hours: ').strip()
                time2 = input('Please Enter End Hours: ').strip()
                comptime1 = datetime.datetime(2022, 1, 1, int(time1[:2]), int(time1[2:]))
                comptime2 = datetime.datetime(2022, 1, 1, int(time2[:2]), int(time2[2:]))
                # Check for time format
                if (time1.isdigit() and time2.isdigit()) and (len(time1) == 4 and len(time2) == 4):

                    interface_text(time1, time2)
                    # Check if the time is before or after package address correction is needed and displays
                    # address correction notification
                    address_correct(comptime1, comptime2)
                    all_truck_packages_status(time1, time2)
                    print("")
                # Else statement for incorrect time format
                else:
                    print("")
                    print('Please Enter Correct Times')
                    print("")
            except ValueError:
                print("")
                print('Please Enter Correct Times')
                print("")
        # If user inputs 2 for individual package status
        if int(choice) == 2:
            package_num = input('Please Enter Package Number: ').strip()
            # Checks if package number is numeric and if package ID is within the 40 packages
            if package_num.isdigit() and (0 < int(package_num) <= 40):
                print("")
                print(time_message)
                print("")

                try:
                    time1 = input('Please Enter Start Hours: ')
                    time2 = input('Please Enter End Hours: ')
                    comptime1 = datetime.datetime(2022, 1, 1, int(time1[:2]), int(time1[2:]))
                    comptime2 = datetime.datetime(2022, 1, 1, int(time2[:2]), int(time2[2:]))
                    # Check for time format
                    if (time1.isdigit() and time2.isdigit()) and (len(time1) == 4 and len(time2) == 4):

                        interface_text(time1, time2)
                        # Check if package ID is 9 and displays correct address notification
                        if int(package_num) == 9:
                            address_correct(comptime1, comptime2)
                        status_of_package(package_num, package_hash, time1, time2)
                        print("")
                    # Else statement for incorrect time format
                    else:
                        print("")
                        print('Please Enter Correct Times')
                        print("")
                except ValueError:
                    print("")
                    print('Please Enter Correct Times')
                    print("")
            else:
                print("")
                print('Package Not Found')
        # If user inputs 3 for total miles
        if int(choice) == 3:
            total_truck_mileage(truck1, truck2, truck3)
            print("")

        print("")
        choice_repeat()
    # Else statement for any other user inputs other than 1 through 3
    else:
        print("")
        print('Please select a value from the choice list')
        print("")
        choice_prompt()
