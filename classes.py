import csv
import datetime

# Time
# Start time for package delivery
start_time = datetime.datetime(2022, 1, 1, 8, 00)
# Correction time of package
correction_time = datetime.datetime(2022, 1, 1, 10, 20)

"""
The HashTable class will contain the packages being delivered. The chaining hash table will contain methods to insert,
search, and remove items.
"""


# HashTable class using chaining.
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def insert(self, key, item):
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Update key if it is already in the bucket
        for key_value in bucket_list:
            # Print (key value)
            if key_value[0] == key:
                key_value[1] = item
                return True
        # If not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        for key_value in bucket_list:
            # Find the key
            if key_value[0] == key:
                return key_value[1]
        return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for key_value in bucket_list:
            # print(key_value)
            if key_value[0] == key:
                bucket_list.remove([key_value[0], key_value[1]])


"""
The Package class contains information associated with packages such as ID, address, delivery times, status and etc.
The Package class will also contain methods to load package data as well as a method to update packages.
"""


# Package class.
class Package:
    # Constructor
    def __init__(self, ID, address, city, state, zip, deadline, kilo, note, status, deliver_time, start_delivery):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.kilo = kilo
        self.note = note
        self.status = status
        self.deliver_time = deliver_time
        self.start_delivery = start_delivery

    def __str__(self):  # overwrite print(Package) otherwise it will print object reference
        return "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            self.ID, self.address, self.city, self.state, self.zip, self.deadline, self.kilo, self.note, self.status,
            self.deliver_time, self.start_delivery)

    def update_package(self, address, zip, note):
        self.address = address
        self.zip = zip
        self.note = note

    # Load packages from a csv file
    def loading_packages(hashtable):
        # CSV File Name
        with open('files/packageCSV.csv') as packages:
            package_data = csv.reader(packages, delimiter=',')
            next(package_data)  # skip header
            # Loop through package data and create package objects
            for package in package_data:
                package_ID = int(package[0])
                package_address = package[1]
                package_city = package[2]
                package_state = package[3]
                package_zip = package[4]
                package_deadline = package[5]
                package_kilo = package[6]
                package_note = package[7]
                # Contains package status: at the hub, en route, delivered
                package_status = str()
                # Contains when package is delivered
                package_deliver_time = datetime.datetime(2022, 1, 1)
                # Contains when package begins delivery
                package_start_delivery = start_time
                # Package Object
                package = Package(package_ID, package_address, package_city, package_state, package_zip,
                                  package_deadline, package_kilo, package_note, package_status, package_deliver_time,
                                  package_start_delivery)

                # Insert into hashtable
                hashtable.insert(package_ID, package)


"""
The truck class contains the packages and information dealing with times such as start of delivery, return from
delivery and tracks the mileage total of a truck after it has completed delivery. It also contains methods to load or
remove packages.
"""


# Truck Class
class Truck:
    # Constructor
    # Assigns truck packages and delivered packages with empty lists.
    def __init__(self):
        # Contains total packages assigned
        self.truck_packages = []
        # Contains a list of packages delivered
        self.delivered_list = []
        # Contains the time when a truck begins delivery
        self.start_time = start_time
        # Contains the return time of the truck
        self.return_time = datetime
        # Contains total mileage of delivery route
        self.total_mileage = float()

    # Truck Load Packages
    def load_packages(self, package_num, hash_table):
        # Trucks can only accept 16 packages or fewer
        # Append to truck pages and delivered list
        if len(self.truck_packages) <= 16:
            package = hash_table.search(package_num)
            self.truck_packages.append(package)
            self.delivered_list.append(package)
        # If more than 16 packages are attempted
        else:
            print("")
            print("ERROR: PACKAGE OVERLOAD")

    # Truck Remove Package
    def remove_package(self, package_num, hash_table):
        package = hash_table.search(package_num)
        self.truck_packages.remove(package)
