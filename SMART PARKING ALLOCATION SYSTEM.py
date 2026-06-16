import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import heapq
from datetime import datetime

# =========================
# DATABASE
# =========================

conn = sqlite3.connect("parking.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicles(
    vehicle_no TEXT PRIMARY KEY,
    vehicle_type TEXT,
    slot INTEGER,
    entry_time TEXT
)
""")

conn.commit()

# =========================
# AI PARKING SYSTEM
# =========================

class SmartParking:

    def __init__(self):

        self.total_slots = 20

        self.slots = {}

        for i in range(1, 21):

            self.slots[i] = {
                "occupied": False,
                "size": self.get_size(i),
                "ev": True if i in [4,8,12,16,20] else False
            }

        self.load_database()

    def get_size(self, slot):

        if slot <= 6:
            return "Small"

        elif slot <= 14:
            return "Medium"

        else:
            return "Large"

    def load_database(self):

        cursor.execute("SELECT slot FROM vehicles")

        records = cursor.fetchall()

        for r in records:
            self.slots[r[0]]["occupied"] = True

    # ----------------------
    # CSP Constraints
    # ----------------------

    def valid_slots(self, vehicle_type):

        valid = []

        for slot,data in self.slots.items():

            if data["occupied"]:
                continue

            if vehicle_type == "EV":

                if not data["ev"]:
                    continue

            if vehicle_type in ["Truck","Bus"]:

                if data["size"] != "Large":
                    continue

            if vehicle_type == "SUV":

                if data["size"] == "Small":
                    continue

            valid.append(slot)

        return valid

    # ----------------------
    # A* Search
    # ----------------------

    def allocate_slot(self,
                      vehicle_type,
                      entry_gate):

        valid = self.valid_slots(vehicle_type)

        if not valid:
            return None

        pq = []

        for slot in valid:

            cost = abs(slot-entry_gate)

            heapq.heappush(
                pq,
                (cost,slot)
            )

        return heapq.heappop(pq)[1]

    # ----------------------
    # Park Vehicle
    # ----------------------

    def park(self,
             vehicle_no,
             vehicle_type,
             entry_gate):

        cursor.execute(
            "SELECT * FROM vehicles WHERE vehicle_no=?",
            (vehicle_no,)
        )

        if cursor.fetchone():

            return "DUPLICATE"

        slot = self.allocate_slot(
            vehicle_type,
            entry_gate
        )

        if slot is None:
            return None

        self.slots[slot]["occupied"] = True

        cursor.execute("""
        INSERT INTO vehicles
        VALUES(?,?,?,?)
        """,
        (
            vehicle_no,
            vehicle_type,
            slot,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

        return slot

    # ----------------------
    # Remove Vehicle
    # ----------------------

    def remove(self,
               vehicle_no):

        cursor.execute(
            "SELECT slot FROM vehicles WHERE vehicle_no=?",
            (vehicle_no,)
        )

        data = cursor.fetchone()

        if not data:
            return False

        slot = data[0]

        self.slots[slot]["occupied"] = False

        cursor.execute(
            "DELETE FROM vehicles WHERE vehicle_no=?",
            (vehicle_no,)
        )

        conn.commit()

        return True

    # ----------------------
    # Search Vehicle
    # ----------------------

    def search(self,
               vehicle_no):

        cursor.execute(
            "SELECT * FROM vehicles WHERE vehicle_no=?",
            (vehicle_no,)
        )

        return cursor.fetchone()

    # ----------------------
    # Report
    # ----------------------

    def report(self):

        occupied = 0

        for slot in self.slots.values():

            if slot["occupied"]:
                occupied += 1

        available = self.total_slots - occupied

        return occupied,available


# =========================
# GUI
# =========================

parking = SmartParking()

root = tk.Tk()
root.title("AI Smart Parking System")
root.geometry("1300x800")

title = tk.Label(
    root,
    text="AI SMART PARKING SYSTEM",
    font=("Arial",24,"bold")
)

title.pack(pady=10)

# =========================
# INPUT FRAME
# =========================

frame = tk.Frame(root)
frame.pack()

tk.Label(frame,text="Vehicle No").grid(row=0,column=0)

vehicle_no = tk.Entry(frame,width=20)
vehicle_no.grid(row=0,column=1)

tk.Label(frame,text="Vehicle Type").grid(row=0,column=2)

vehicle_type = ttk.Combobox(
    frame,
    values=[
        "Bike",
        "Car",
        "SUV",
        "Truck",
        "Bus",
        "EV"
    ]
)

vehicle_type.current(0)
vehicle_type.grid(row=0,column=3)

tk.Label(frame,text="Entry Gate").grid(row=0,column=4)

entry_gate = tk.Entry(frame,width=10)
entry_gate.insert(0,"1")
entry_gate.grid(row=0,column=5)

# =========================
# OUTPUT
# =========================

output = tk.Text(
    root,
    height=12,
    width=120
)

output.pack(pady=20)

# =========================
# SLOT GRID
# =========================

grid_frame = tk.Frame(root)
grid_frame.pack()

slot_labels = {}

for i in range(1,21):

    lbl = tk.Label(
        grid_frame,
        text=f"Slot {i}",
        width=12,
        height=4,
        relief="ridge",
        bg="lightgreen"
    )

    lbl.grid(
        row=(i-1)//5,
        column=(i-1)%5,
        padx=5,
        pady=5
    )

    slot_labels[i] = lbl

def update_grid():

    for slot,data in parking.slots.items():

        if data["occupied"]:

            slot_labels[slot].config(
                bg="tomato",
                text=f"Slot {slot}\nOccupied"
            )

        else:

            slot_labels[slot].config(
                bg="lightgreen",
                text=f"Slot {slot}\nAvailable"
            )

# =========================
# BUTTON FUNCTIONS
# =========================

def park_vehicle():

    try:

        number = vehicle_no.get()
        vtype = vehicle_type.get()
        gate = int(entry_gate.get())

        slot = parking.park(
            number,
            vtype,
            gate
        )

        if slot == "DUPLICATE":

            messagebox.showwarning(
                "Warning",
                "Vehicle already exists"
            )

            return

        if slot is None:

            messagebox.showerror(
                "Error",
                "No Slot Available"
            )

            return

        output.insert(
            tk.END,
            f"\nAI Decision\n"
            f"Vehicle: {number}\n"
            f"Type: {vtype}\n"
            f"Allocated Slot: {slot}\n"
            f"CSP Applied ✓\n"
            f"A* Search Applied ✓\n"
        )

        update_grid()

    except:
        messagebox.showerror(
            "Error",
            "Invalid Input"
        )

def remove_vehicle():

    if parking.remove(
        vehicle_no.get()
    ):

        output.insert(
            tk.END,
            "\nVehicle Removed\n"
        )

        update_grid()

    else:

        messagebox.showerror(
            "Error",
            "Vehicle Not Found"
        )

def search_vehicle():

    data = parking.search(
        vehicle_no.get()
    )

    if data:

        output.insert(
            tk.END,
            f"\nVehicle Found\n"
            f"{data}\n"
        )

    else:

        messagebox.showerror(
            "Error",
            "Vehicle Not Found"
        )

def report():

    occ,avl = parking.report()

    output.insert(
        tk.END,
        f"\n===== REPORT =====\n"
        f"Occupied : {occ}\n"
        f"Available : {avl}\n"
    )

# =========================
# BUTTONS
# =========================

btn = tk.Frame(root)
btn.pack()

tk.Button(
    btn,
    text="AI Allocate",
    command=park_vehicle,
    width=15
).grid(row=0,column=0,padx=5)

tk.Button(
    btn,
    text="Search",
    command=search_vehicle,
    width=15
).grid(row=0,column=1,padx=5)

tk.Button(
    btn,
    text="Remove",
    command=remove_vehicle,
    width=15
).grid(row=0,column=2,padx=5)

tk.Button(
    btn,
    text="Report",
    command=report,
    width=15
).grid(row=0,column=3,padx=5)

update_grid()

root.mainloop()