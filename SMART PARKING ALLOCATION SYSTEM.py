# SMART PARKING ALLOCATION SYSTEM

class SmartParkingSystem:
    def __init__(self):
        self.slots = {}
        self.total_slots = 0

    # Add parking slots
    def add_slots(self, count):
        start = self.total_slots + 1
        self.total_slots += count

        for i in range(start, self.total_slots + 1):
            self.slots[i] = None

        print(f"\n{count} parking slots added successfully!")

    # Auto allocate slot
    def auto_allocate(self, vehicle_no, vehicle_type):
        for slot in self.slots:
            if self.slots[slot] is None:
                self.slots[slot] = {
                    "number": vehicle_no,
                    "type": vehicle_type
                }
                print(f"\nVehicle parked successfully in Slot {slot}")
                return

        print("\nParking Full!")

    # Choose slot manually
    def choose_slot(self, vehicle_no, vehicle_type, slot_no):
        if slot_no not in self.slots:
            print("\nInvalid Slot Number!")
            return

        if self.slots[slot_no] is None:
            self.slots[slot_no] = {
                "number": vehicle_no,
                "type": vehicle_type
            }
            print(f"\nVehicle parked in Slot {slot_no}")
        else:
            print("\nSlot Already Occupied!")

    # Remove vehicle
    def remove_vehicle(self, vehicle_no):
        for slot in self.slots:
            if self.slots[slot] and self.slots[slot]["number"] == vehicle_no:
                self.slots[slot] = None
                print(f"\nVehicle removed from Slot {slot}")
                return

        print("\nVehicle Not Found!")

    # Search vehicle
    def search_vehicle(self, vehicle_no):
        for slot in self.slots:
            if self.slots[slot] and self.slots[slot]["number"] == vehicle_no:
                print(f"\nVehicle Found!")
                print(f"Slot Number : {slot}")
                print(f"Vehicle Type : {self.slots[slot]['type']}")
                return

        print("\nVehicle Not Found!")

    # Display all slots
    def display_slots(self):
        print("\n========== PARKING STATUS ==========")

        if self.total_slots == 0:
            print("No slots available.")
            return

        for slot in self.slots:
            if self.slots[slot]:
                print(
                    f"Slot {slot} --> "
                    f"{self.slots[slot]['number']} "
                    f"({self.slots[slot]['type']})"
                )
            else:
                print(f"Slot {slot} --> Empty")

    # Available slots
    def available_slots(self):
        print("\nAvailable Slots:")

        count = 0

        for slot in self.slots:
            if self.slots[slot] is None:
                print(slot, end=" ")
                count += 1

        print(f"\nTotal Available Slots: {count}")

    # Occupied slots
    def occupied_slots(self):
        print("\nOccupied Slots:")

        found = False

        for slot in self.slots:
            if self.slots[slot]:
                found = True
                print(
                    f"Slot {slot} --> "
                    f"{self.slots[slot]['number']} "
                    f"({self.slots[slot]['type']})"
                )

        if not found:
            print("No Occupied Slots")

    # Parking report
    def parking_report(self):
        occupied = 0

        for slot in self.slots.values():
            if slot:
                occupied += 1

        available = self.total_slots - occupied

        print("\n========== PARKING REPORT ==========")
        print("Total Slots     :", self.total_slots)
        print("Occupied Slots  :", occupied)
        print("Available Slots :", available)


# Main Program
parking = SmartParkingSystem()

while True:

    print("\n")
    print("======================================")
    print(" SMART PARKING ALLOCATION SYSTEM ")
    print("======================================")
    print("1. Add Parking Slots")
    print("2. Park Vehicle (Auto)")
    print("3. Park Vehicle (Choose Slot)")
    print("4. Remove Vehicle")
    print("5. Search Vehicle")
    print("6. Display All Slots")
    print("7. Show Available Slots")
    print("8. Show Occupied Slots")
    print("9. Parking Report")
    print("10. Exit")

    choice = input("\nEnter Your Choice: ")

    # Add slots
    if choice == "1":
        count = int(input("Enter Number of Slots: "))
        parking.add_slots(count)

    # Auto parking
    elif choice == "2":

        vehicle_no = input("Enter Vehicle Number: ")

        print("\nVehicle Types")
        print("1. Bike")
        print("2. Car")
        print("3. SUV")
        print("4. Bus")
        print("5. Truck")
        print("6. EV")

        v = input("Choose Vehicle Type: ")

        types = {
            "1": "Bike",
            "2": "Car",
            "3": "SUV",
            "4": "Bus",
            "5": "Truck",
            "6": "EV"
        }

        vehicle_type = types.get(v, "Car")

        parking.auto_allocate(vehicle_no, vehicle_type)

    # Manual slot selection
    elif choice == "3":

        vehicle_no = input("Enter Vehicle Number: ")

        print("\nVehicle Types")
        print("1. Bike")
        print("2. Car")
        print("3. SUV")
        print("4. Bus")
        print("5. Truck")
        print("6. EV")

        v = input("Choose Vehicle Type: ")

        types = {
            "1": "Bike",
            "2": "Car",
            "3": "SUV",
            "4": "Bus",
            "5": "Truck",
            "6": "EV"
        }

        vehicle_type = types.get(v, "Car")

        slot_no = int(input("Enter Slot Number: "))

        parking.choose_slot(vehicle_no, vehicle_type, slot_no)

    # Remove vehicle
    elif choice == "4":
        vehicle_no = input("Enter Vehicle Number: ")
        parking.remove_vehicle(vehicle_no)

    # Search vehicle
    elif choice == "5":
        vehicle_no = input("Enter Vehicle Number: ")
        parking.search_vehicle(vehicle_no)

    # Display slots
    elif choice == "6":
        parking.display_slots()

    # Available slots
    elif choice == "7":
        parking.available_slots()

    # Occupied slots
    elif choice == "8":
        parking.occupied_slots()

    # Report
    elif choice == "9":
        parking.parking_report()

    # Exit
    elif choice == "10":
        print("\nThank You For Using Smart Parking System!")
        break

    else:
        print("\nInvalid Choice! Please Try Again.")