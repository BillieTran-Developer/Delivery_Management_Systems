import datetime

import classes
from classes import *
from functions import *

# Variables
# Hash Table Instance
package_hash = ChainingHashTable()
# Loading Hash Table with Data
Package.loading_packages(package_hash)
# Trucks
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()

# Truck 1 Loads

# Packages Must Be Together Loads
truck1.load_packages(13, package_hash)
truck1.load_packages(14, package_hash)
truck1.load_packages(15, package_hash)
truck1.load_packages(16, package_hash)
truck1.load_packages(19, package_hash)
truck1.load_packages(20, package_hash)
# Other Packages
truck1.load_packages(1, package_hash)
truck1.load_packages(2, package_hash)
truck1.load_packages(4, package_hash)
truck1.load_packages(5, package_hash)
truck1.load_packages(7, package_hash)
truck1.load_packages(8, package_hash)
truck1.load_packages(10, package_hash)
truck1.load_packages(11, package_hash)
truck1.load_packages(30, package_hash)
truck1.load_packages(40, package_hash)


# Truck 2 Loads
# Truck 2 Only Loads
truck2.load_packages(3, package_hash)
truck2.load_packages(18, package_hash)
truck2.load_packages(36, package_hash)
truck2.load_packages(38, package_hash)
# Other Packages
truck2.load_packages(12, package_hash)
truck2.load_packages(17, package_hash)
truck2.load_packages(21, package_hash)
truck2.load_packages(22, package_hash)
truck2.load_packages(23, package_hash)
truck2.load_packages(24, package_hash)
truck2.load_packages(26, package_hash)
truck2.load_packages(27, package_hash)
truck2.load_packages(37, package_hash)
truck2.load_packages(39, package_hash)
truck2.load_packages(29, package_hash)

# Truck 3 Loads

# Packages cannot leave hub before 0905
truck3.load_packages(6, package_hash)
truck3.load_packages(25, package_hash)
truck3.load_packages(28, package_hash)
truck3.load_packages(32, package_hash)
# Other Packages
truck3.load_packages(31, package_hash)
truck3.load_packages(33, package_hash)
truck3.load_packages(34, package_hash)
truck3.load_packages(35, package_hash)
truck3.load_packages(9, package_hash)

# Dispatch Trucks
truck_hub(truck1, truck2, truck3)
