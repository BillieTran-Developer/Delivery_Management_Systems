import csv
from datetime import datetime
import classes
from classes import *

# Data Lists
distance_data = []
address_data = []

# Data Functions
"""
The function loading_distances loads data from a csv file to a list.
"""


def loading_distances(distance_data_list):
    with open('files/distanceCSV.csv') as distances:
        distance_data = csv.reader(distances, delimiter=',')
        next(distance_data)
        for row in distance_data:
            distance_data_list.append(row)


"""
The function loading_addresses loads data from a csv file to a list.
"""


def loading_addresses(address_data_list):
    with open('files/addressCSV.csv') as addresses:
        address_data = csv.reader(addresses, delimiter=',')
        next(address_data)
        for address in address_data:
            address_data_list.append(address[0])


# Loading Data Lists
loading_distances(distance_data)
loading_addresses(address_data)

# Distance Functions
"""
The function distance_between finds the distance between two points by using the indexes found from the address 
data file to transverse through the distance data file. 
"""


def distance_between(address1, address2):
    data = distance_data
    address = address_data

    # Find the index of both addresses from the address data list
    address1_index = address.index(address1)
    address2_index = address.index(address2)
    # Through the indexes find the distance between the two points using the distance data list
    distance = float(data[address1_index][address2_index])

    return distance


"""
The function minimum_distance finds the minimum distance between two points by looping through a list of distances. 
"""


def minimum_distance(from_address, truck_packages):
    # List that will contain packages distances between parameter from_address and packages from truck_packages
    package_distance = []
    distance = float()
    # Loop through truck_packages, adding the distances to package_distance
    for package in truck_packages:
        if from_address != package.ID:
            distance = distance_between(from_address, package.address)
            package_distance.append(float(distance))
    # Return the min
    return min(package_distance)


# Delivery Function
"""
The function truck_deliveries is the algorithm used to deliver the packages found in a truck. The function 
utilizes the nearest neighbor algorithm to deliver the packages. The function is also responsible for time and 
location tracking, tracking the time of package delivery as well as marking the status as delivered, the miles driven 
and when delivery is complete the function also returns the truck back to the hub. The function is also responsible 
for the address correction for package 9.
"""


def truck_deliveries(truck):
    packages = truck.truck_packages
    packages_left = len(packages)
    time_total = datetime.timedelta()
    delivered_time = truck.start_time
    hub = '4001 South 700 East'
    current_location = hub
    miles_driven = float()

    while packages_left > 0:
        # Finding the minimum distance between the current location and other possible next delivery locations
        min_distance = minimum_distance(current_location, packages)
        # Looping package from packages
        for package in packages:
            # Checks if the distance between package equals the package with the minimum distance as well as the
            # package status.
            if distance_between(current_location, package.address) == min_distance and package.status != 'Delivered':
                # Assigns the distance driven to the variable miles
                miles = distance_between(current_location, package.address)
                # Add to total miles driven
                miles_driven += miles
                # Update package status once minimum distance is found
                package.status = 'Delivered'
                # Remove package from packages on truck
                truck.truck_packages.remove(package)
                # Calculates the time driven using the truck speed of 18mph and converts it to hours
                time_to_deliver = datetime.timedelta(hours=min_distance / 18)
                # Add to total time for deliveries
                time_total += time_to_deliver
                # Converts to military time
                delivered_time += time_to_deliver
                # Creates the delivery time for packages
                package.deliver_time = delivered_time
                # Changes current location to the minimum location found
                current_location = package.address
                # If statement that compares the current time to correction time for package 9
                if package.deliver_time >= correction_time:
                    if package.ID == 9:
                        package.update_package('410 S State St', '84111', 'Address has been corrected')

                break

        # Decrement package count
        packages_left -= 1

        # If statement for when there are no packages left on truck
        if packages_left == 0:
            # Find the distance between current location and hub
            return_hub = distance_between(current_location, hub)
            # Add return distance to total miles driven
            miles_driven += return_hub
            # Add miles driven to truck.total_mileage
            truck.total_truck_mileage = miles_driven
            # Calculates the time driven using the truck speed of 18mph and converts it to hours
            time_to_return = datetime.timedelta(hours=return_hub / 18)
            # Add to total time for deliveries
            time_total += time_to_deliver
            # Return current location back to hub
            current_location = hub
            # Converts to military time
            truck.return_time = truck.start_time + time_total


"""
The function truck_hub is responsible for dispatching the trucks. There are 3 trucks and only 2 drivers, 
truck_hub dispatches the initial 2 trucks, and tracks how many packages per truck. Once the 
truck is empty and returned from it's route, truck_station then dispatches truck3 for delivery while setting the start
time for truck3 and the packages on truck3.
"""


def truck_hub(truck1, truck2, truck3):
    # Call truck_deliver_packages function
    # truck1 and truck2 dispatched
    truck_deliveries(truck1)
    truck_deliveries(truck2)
    # Checks truck for empty packages
    if len(truck1.truck_packages) == 0 or len(truck2.truck_packages) == 0:
        # Sets the start time for truck 3 depending on which truck returns first
        if truck1.return_time > truck2.return_time:

            truck3.start_time = truck2.return_time

        elif truck2.return_time > truck1.return_time:

            truck3.start_time = truck1.return_time

            # Sets the package start delivery time for truck3
            for package in truck3.truck_packages:
                package.start_delivery = truck1.return_time
        # Call truck_deliver_packages function
        # truck3 dispatched
        truck_deliveries(truck3)


# Package Functions
"""
The function status_of_packages creates a snapshot of the status of packages between two time points to find out the 
times for at the hub, en route, and delivered. The function loops through the delivery list and through certain time 
conditions labels package statuses and appends them to a snapshot list. The snapshot list is then printed onto the 
console. 
"""


def status_of_packages(truck, time1, time2):
    start_time = classes.start_time

    # Checks times are entered correctly
    if time1 <= time2:

        truck_start_time = truck.start_time.replace(second=0)
        stringify_time1 = str(time1)
        hours1 = stringify_time1[:2]
        minutes1 = stringify_time1[2:]
        stringify_time2 = str(time2)
        hours2 = stringify_time2[:2]
        minutes2 = stringify_time2[2:]
        time1 = datetime.datetime(2022, 1, 1, int(hours1), int(minutes1)).replace(second=0)
        time2 = datetime.datetime(2022, 1, 1, int(hours2), int(minutes2)).replace(second=0)
        snapshot = []

        for package in sorted(truck.delivered_list, key=lambda package: package.ID):
            deliver_time = package.deliver_time.replace(second=0)
            # Checking conditions to update status for at the hub time
            if (time1 < truck_start_time and time2 <= truck_start_time) or (time1 < start_time and time2 < start_time):
                package.status = 'At the Hub'
                snapshot.append(package)

            # Checking conditions to update status for en route
            elif (time1 >= truck_start_time and time2 < deliver_time) or (truck_start_time < time2 < deliver_time):
                package.status = 'En Route'
                snapshot.append(package)
            # Checking conditions to update status for delivered
            elif (time2 >= deliver_time) or (time1 >= deliver_time and time2 > deliver_time):
                package.status = 'Delivered'
                snapshot.append(package)

        # Print snapshot
        for package in snapshot:
            # Checks package status for 'Delivered', delivered packages print out the delivered time
            if package.status == 'Delivered':
                print('{:10s} {:45.45s}    {:20.20s}     {:10s} {:10s} {}       {}'.format(str(package.ID),
                                                                                           package.address,
                                                                                           package.city,
                                                                                           package.state,
                                                                                           package.zip,
                                                                                           package.status,
                                                                                           package.deliver_time))
            # Packages that are not delivered do not print anything within the delivered column
            else:
                print('{:10s} {:45.45s}    {:20.20s}     {:10s} {:10s} {}'.format(str(package.ID),
                                                                                  package.address,
                                                                                  package.city, package.state,
                                                                                  package.zip,
                                                                                  package.status))


"""
The function status_of_package creates a snapshot of the status of package by id. The function checks certain 
time conditions labels package statuses and appends them to a snapshot list. The snapshot list is then printed 
onto the console. 
"""


def status_of_package(package_ID, hashtable, time1, time2):
    start_time = datetime.datetime(2022, 1, 1, 8, 00)
    package = hashtable.search(int(package_ID))

    if time1 <= time2:

        package_start_time = package.start_delivery.replace(second=0)
        delivery_time = package.deliver_time.replace(second=0)
        stringify_time1 = str(time1)
        hours1 = stringify_time1[:2]
        minutes1 = stringify_time1[2:]
        stringify_time2 = str(time2)
        hours2 = stringify_time2[:2]
        minutes2 = stringify_time2[2:]
        time1 = datetime.datetime(2022, 1, 1, int(hours1), int(minutes1)).replace(second=0)
        time2 = datetime.datetime(2022, 1, 1, int(hours2), int(minutes2)).replace(second=0)

        # Checking conditions to update for hub time
        if (time1 < package_start_time and time2 < package_start_time) or (time1 < start_time and time2 < start_time):
            package.status = 'At the Hub'

        # Checking conditions to update en route
        elif (time1 >= package_start_time and time2 < delivery_time) or (package_start_time < time2 < delivery_time):
            package.status = 'En Route'

        # Checking conditions to update delivery
        elif (time2 > delivery_time) or (time1 >= delivery_time and time2 > delivery_time):
            package.status = 'Delivered'

            # Checks package status for 'Delivered', delivered packages print out the delivered time
        if package.status == 'Delivered':
            print('{:10s} {:45.45s}    {:20.20s}     {:10s} {:10s} {}       {}'.format(str(package.ID), package.address,
                                                                                       package.city, package.state,
                                                                                       package.zip, package.status,
                                                                                       package.deliver_time))
            # Packages that are not delivered do not print anything within the delivered column
        else:
            print(
                '{:10s} {:45.45s}    {:20.20s}     {:10s} {:10s} {}'.format(str(package.ID), package.address,
                                                                            package.city, package.state, package.zip,
                                                                            package.status))


"""
The function address_display displays the corrected addresses of a package.
"""


def address_display(package_ID, hashtable, address, city, state, zip, note):
    # Search package ID
    package = hashtable.search(int(package_ID))
    # Sets package address to correct address
    package.address = address
    package.city = city
    package.state = state
    package.zip = zip
    package.note = note
