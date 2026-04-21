# ╔══════════════════════════════════════════════════════════════╗
# ║           ParkEase — Parking Lot Management System           ║
# ╚══════════════════════════════════════════════════════════════╝

from datetime import datetime

# ── Configuration ─────────────────────────────────────────────────────────────
TOTAL_SLOTS = 10

# ── Global State ──────────────────────────────────────────────────────────────
# All slots start as available (True = free, False = occupied)
slots = {i: True for i in range(1, TOTAL_SLOTS + 1)}

# Master parking records dictionary
# Key: vehicle_number  →  Value: record dict
parking_records = {}


# ── Helpers ───────────────────────────────────────────────────────────────────
def now():
    return datetime.now().strftime("%d-%m-%Y  %H:%M:%S")

def available_count():
    return sum(1 for v in slots.values() if v)

def next_free_slot():
    for slot_num, is_free in slots.items():
        if is_free:
            return slot_num
    return None

def banner():
    free = available_count()
    occupied = TOTAL_SLOTS - free
    print("\n" + "=" * 54)
    print("        ParkEase -- Parking Lot Management")
    print("=" * 54)
    print(f"  Total Slots    : {TOTAL_SLOTS}")
    print(f"  Available      : {free}")
    print(f"  Occupied       : {occupied}")
    print("  " + "-" * 24)
    # Visual slot map
    row = "  Slots : "
    for i in range(1, TOTAL_SLOTS + 1):
        if slots[i]:
            row += f"[{i:02d}:FREE] "
        else:
            row += f"[{i:02d}:BUSY] "
        if i == 5:
            print(row)
            row = "         "
    print(row)
    print("=" * 54)

def show_action_menu():
    print("\n  What would you like to do?")
    print("    [1]  Vehicle Entry  (assign a slot)")
    print("    [2]  Vehicle Exit   (free a slot)")

# ── Vehicle Entry ─────────────────────────────────────────────────────────────
def vehicle_entry(name, vehicle_number):
    # Check if slots are full
    if available_count() == 0:
        print("\n  !! Slots full. Cannot allow entry at this time.\n")
        return

    # Check: vehicle already parked
    if vehicle_number in parking_records and parking_records[vehicle_number]["exit_date"] is None:
        rec = parking_records[vehicle_number]
        print(f"\n  [!] Vehicle {vehicle_number} is already parked at Slot {rec['slot']}.\n")
        return

    slot = next_free_slot()
    slots[slot] = False          # mark slot as occupied
    entry_time  = now()

    parking_records[vehicle_number] = {
        "name":         name,
        "vehicle_number": vehicle_number,
        "slot":         slot,
        "entry_date":   entry_time,
        "exit_date":    None,
    }

    print(f"\n  [+] Entry Successful!")
    print(f"      Name           : {name}")
    print(f"      Vehicle Number : {vehicle_number}")
    print(f"      Slot Assigned  : {slot}")
    print(f"      Entry Time     : {entry_time}")
    print(f"      Slots Left     : {available_count()}/{TOTAL_SLOTS}\n")

# ── Vehicle Exit ──────────────────────────────────────────────────────────────
def vehicle_exit():
    identifier = input("  Enter Name or Vehicle Number to exit: ").strip()
    if not identifier:
        print("  [!] Input cannot be empty.")
        return

    # Search by vehicle number first, then by name
    found_key = None
    for vnum, rec in parking_records.items():
        if (vnum.upper() == identifier.upper() or
                rec["name"].lower() == identifier.lower()):
            if rec["exit_date"] is None:   # still parked
                found_key = vnum
                break

    if not found_key:
        print(f"\n  [!] No active parking record found for '{identifier}'.\n")
        return

    rec       = parking_records[found_key]
    exit_time = now()
    slot      = rec["slot"]

    # Free the slot
    slots[slot]      = True
    rec["exit_date"] = exit_time

    print(f"\n  [-] Exit Successful!")
    print(f"      Name           : {rec['name']}")
    print(f"      Vehicle Number : {rec['vehicle_number']}")
    print(f"      Slot Freed     : {slot}")
    print(f"      Entry Time     : {rec['entry_date']}")
    print(f"      Exit Time      : {exit_time}")
    print(f"      Slots Available: {available_count()}/{TOTAL_SLOTS}\n")

# ── View All Records ──────────────────────────────────────────────────────────
def view_all_records():
    if not parking_records:
        print("\n  No records found.\n")
        return
    print("\n" + "=" * 80)
    print(f"  {'Vehicle No':<14} {'Name':<16} {'Slot':>4}  {'Entry':<20}  {'Exit'}")
    print("  " + "-" * 76)
    for vnum, rec in parking_records.items():
        exit_str = rec["exit_date"] if rec["exit_date"] else "-- still parked --"
        print(f"  {vnum:<14} {rec['name']:<16} {rec['slot']:>4}  "
              f"{rec['entry_date']:<20}  {exit_str}")
    print("=" * 80)

# ── Return Dictionary ─────────────────────────────────────────────────────────
def return_dictionary():
    print("\n" + "=" * 54)
    print("  PARKING RECORDS DICTIONARY")
    print("=" * 54)
    if not parking_records:
        print("  (empty)")
    for vnum, data in parking_records.items():
        print(f"\n  {vnum}:")
        for k, v in data.items():
            val = v if v is not None else "N/A"
            print(f"      {k:<18}: {val}")
    print("\n" + "=" * 54)
    return parking_records


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "=" * 54)
    print("   Welcome to ParkEase Parking Lot System")
    print("=" * 54)

    while True:
        banner()
        print("\n  Enter vehicle details  (or type 'done' to exit)")

        name = input("\n  Owner Name      : ").strip()
        if name.lower() == "done":
            break
        if not name:
            print("  [!] Name cannot be empty.")
            continue

        vehicle_number = input("  Vehicle Number  : ").strip().upper()
        if vehicle_number == "DONE":
            break
        if not vehicle_number:
            print("  [!] Vehicle number cannot be empty.")
            continue

        show_action_menu()
        action = input("\n  Your choice [1/2]: ").strip()

        if action == "1":
            vehicle_entry(name, vehicle_number)
        elif action == "2":
            vehicle_exit()
        else:
            print("  [!] Invalid choice. Enter 1 or 2.")

    # ── Exit Summary ──────────────────────────────────────────────────────────
    print("\n  Session ended. Here is the full parking log:")
    view_all_records()

    return return_dictionary()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = main()
    # `result` holds the full parking_records dictionary
