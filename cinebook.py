# ╔══════════════════════════════════════════════════════════════════╗
# ║           CineBook — Movie Ticket Booking System                 ║
# ╚══════════════════════════════════════════════════════════════════╝

from datetime import datetime

# ── Screen Configuration ───────────────────────────────────────────────────────
SCREENS = {
    1: {
        "movie":    "Pushpa 2: The Rule",
        "rows":     6,          # A–F
        "cols":     5,          # 1–5   →  30 seats
        "price":    350,
        "total":    30,
    },
    2: {
        "movie":    "Rajasaab",
        "rows":     5,          # A–E
        "cols":     5,          # 1–5   →  25 seats
        "price":    200,
        "total":    25,
    },
}

# ── Global State ───────────────────────────────────────────────────────────────
# seat_map[screen_no][seat_id] = None (free) or ticket_number (occupied)
seat_map = {}
for sno, cfg in SCREENS.items():
    seat_map[sno] = {}
    for r in range(cfg["rows"]):
        for c in range(1, cfg["cols"] + 1):
            seat_id = f"{chr(65 + r)}{c}"
            seat_map[sno][seat_id] = None

bookings      = {}   # { ticket_number : record }
ticket_counter = 1
cancel_counter = 1


# ── ID Generators ──────────────────────────────────────────────────────────────
def new_ticket_id():
    global ticket_counter
    tid = f"TKT{ticket_counter:04d}"
    ticket_counter += 1
    return tid

def new_cancel_id():
    global cancel_counter
    cid = f"CXL{cancel_counter:04d}"
    cancel_counter += 1
    return cid

def now():
    return datetime.now().strftime("%d-%m-%Y  %H:%M")


# ── Visual Seat Map ────────────────────────────────────────────────────────────
def display_seats(screen_no):
    cfg  = SCREENS[screen_no]
    smap = seat_map[screen_no]
    free = sum(1 for v in smap.values() if v is None)

    print(f"\n  ╔{'═'*54}╗")
    print(f"  ║   SCREEN {screen_no}  —  {cfg['movie']:<30}      ║")
    print(f"  ║   Price: Rs{cfg['price']}  |  Available: {free}/{cfg['total']}           ║")
    print(f"  ╠{'═'*54}╣")
    print(f"  ║                   [ SCREEN / STAGE ]              ║")
    print(f"  ╠{'═'*54}╣")

    for r in range(cfg["rows"]):
        row_label = chr(65 + r)
        row_str   = f"  ║  {row_label}  "
        for c in range(1, cfg["cols"] + 1):
            seat_id = f"{row_label}{c}"
            if smap[seat_id] is None:
                row_str += f"[{seat_id}] "
            else:
                row_str += f" XX  "     # booked seat
        # pad to fixed width
        row_str += " " * (55 - len(row_str)) + "║"
        print(row_str)

    print(f"  ╠{'═'*54}╣")
    print(f"  ║   [seat] = Available      XX = Booked              ║")
    print(f"  ╚{'═'*54}╝")


# ── Available Seats Helper ─────────────────────────────────────────────────────
def free_seats(screen_no):
    return [sid for sid, owner in seat_map[screen_no].items() if owner is None]

def available_count(screen_no):
    return len(free_seats(screen_no))


# ── Print Booking Ticket ───────────────────────────────────────────────────────
def print_ticket(record):
    seats_str  = ", ".join(record["seat_numbers"])
    print(f"\n  {'*'*54}")
    print(f"  *{'CineBook -- BOOKING CONFIRMATION':^52}*")
    print(f"  {'*'*54}")
    print(f"  * Ticket No     : {record['ticket_number']:<34}*")
    print(f"  * Name          : {record['name']:<34}*")
    print(f"  * Mobile        : {record['mobile']:<34}*")
    print(f"  * Movie         : {record['movie']:<34}*")
    print(f"  * Screen        : {record['screen_number']:<34}*")
    print(f"  * Date          : {record['date']:<34}*")
    print(f"  * Seats         : {seats_str:<34}*")
    print(f"  * Total Seats   : {record['total_seats']:<34}*")
    print(f"  * Total Amount  : Rs{record['total_amount']:<32}*")
    print(f"  * Booked On     : {record['booked_on']:<34}*")
    print(f"  {'*'*54}")
    print(f"  Tickets booked successfully.")
    print(f"  {'*'*54}\n")


# ── Print Cancellation Ticket ──────────────────────────────────────────────────
def print_cancel_ticket(record):
    seats_str = ", ".join(record["seat_numbers"])
    cinfo     = record["cancellation"]
    print(f"\n  {'*'*54}")
    print(f"  *{'CineBook -- CANCELLATION RECEIPT':^52}*")
    print(f"  {'*'*54}")
    print(f"  * Cancel Ref    : {cinfo['cancel_id']:<34}*")
    print(f"  * Orig Ticket   : {record['ticket_number']:<34}*")
    print(f"  * Name          : {record['name']:<34}*")
    print(f"  * Movie         : {record['movie']:<34}*")
    print(f"  * Screen        : {record['screen_number']:<34}*")
    print(f"  * Date          : {record['date']:<34}*")
    print(f"  * Seats         : {seats_str:<34}*")
    print(f"  * Refund Amt    : Rs{cinfo['refund_amount']:<32}*")
    print(f"  * Cancelled On  : {cinfo['cancelled_on']:<34}*")
    print(f"  {'*'*54}")
    print(f"  Amount will be refunded in a moment.")
    print(f"  {'*'*54}\n")


# ── Book Seats ─────────────────────────────────────────────────────────────────
def book_seats(name, mobile, date, screen_no):
    cfg = SCREENS[screen_no]

    if available_count(screen_no) == 0:
        print(f"\n  [!] Sorry, Screen {screen_no} ({cfg['movie']}) is fully booked.\n")
        return

    display_seats(screen_no)
    print(f"\n  Enter seat numbers separated by commas  (e.g. A1,B3,C5)")
    raw = input("  Seats to book: ").strip().upper()

    if not raw:
        print("  [!] No seats entered.")
        return

    requested = [s.strip() for s in raw.split(",") if s.strip()]

    # ── Validate ───────────────────────────────────────────────────────────────
    all_seats = seat_map[screen_no]
    errors    = []
    for s in requested:
        if s not in all_seats:
            errors.append(f"{s} is not a valid seat")
        elif all_seats[s] is not None:
            errors.append(f"{s} is already booked")

    # Remove duplicates in request
    if len(requested) != len(set(requested)):
        print("  [!] Duplicate seat numbers in your request. Please re-enter.")
        return

    if errors:
        print("\n  [!] Booking failed due to the following issues:")
        for e in errors:
            print(f"      - {e}")
        return

    # ── Confirm & Book ─────────────────────────────────────────────────────────
    total_amount = len(requested) * cfg["price"]
    print(f"\n  Seats selected : {', '.join(requested)}")
    print(f"  Total Amount   : Rs{total_amount}")
    confirm = input("  Confirm booking? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Booking cancelled by user.")
        return

    tid = new_ticket_id()
    ts  = now()

    for s in requested:
        seat_map[screen_no][s] = tid      # mark as occupied

    record = {
        "ticket_number":   tid,
        "name":            name,
        "mobile":          mobile,
        "date":            date,
        "movie":           cfg["movie"],
        "screen_number":   screen_no,
        "seat_numbers":    requested,
        "total_seats":     len(requested),
        "total_amount":    total_amount,
        "price_per_seat":  cfg["price"],
        "booked_on":       ts,
        "status":          "booked",
        "cancellation":    None,
    }

    bookings[tid] = record
    print_ticket(record)
    print(f"  Remaining seats on Screen {screen_no}: {available_count(screen_no)}/{cfg['total']}")


# ── Cancel Booking ─────────────────────────────────────────────────────────────
def cancel_booking():
    tid = input("\n  Enter Ticket Number to cancel (e.g. TKT0001): ").strip().upper()

    if tid not in bookings:
        print(f"\n  [!] Ticket '{tid}' not found.\n")
        return

    record = bookings[tid]

    if record["status"] == "cancelled":
        print(f"\n  [!] Ticket {tid} has already been cancelled.\n")
        return

    screen_no = record["screen_number"]
    seats     = record["seat_numbers"]

    print(f"\n  Booking found:")
    print(f"  Name    : {record['name']}")
    print(f"  Movie   : {record['movie']}")
    print(f"  Screen  : {screen_no}")
    print(f"  Seats   : {', '.join(seats)}")
    print(f"  Amount  : Rs{record['total_amount']}")

    confirm = input("\n  Confirm cancellation? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Cancellation aborted.")
        return

    # ── Free the seats ─────────────────────────────────────────────────────────
    for s in seats:
        seat_map[screen_no][s] = None

    cid = new_cancel_id()
    ts  = now()

    record["status"] = "cancelled"
    record["cancellation"] = {
        "cancel_id":      cid,
        "cancelled_on":   ts,
        "refund_amount":  record["total_amount"],
        "seats_freed":    seats,
    }

    print_cancel_ticket(record)
    print(f"  Remaining seats on Screen {screen_no}: {available_count(screen_no)}/{SCREENS[screen_no]['total']}")


# ── Show All Bookings ──────────────────────────────────────────────────────────
def view_all_bookings():
    if not bookings:
        print("\n  No bookings yet.\n")
        return
    print("\n" + "=" * 74)
    print(f"  {'Ticket':<10} {'Name':<14} {'Movie':<22} {'Scr':>3}  "
          f"{'Seats':<14} {'Amt':>7}  Status")
    print("  " + "-" * 70)
    for tid, rec in bookings.items():
        seats_str = ",".join(rec["seat_numbers"])
        status    = rec["status"].upper()
        print(f"  {tid:<10} {rec['name']:<14} {rec['movie']:<22} "
              f"{rec['screen_number']:>3}  {seats_str:<14} "
              f"Rs{rec['total_amount']:>5}  {status}")
    print("=" * 74)

def remaining_seats_summary():
    print("\n  Remaining Seats:")
    for sno, cfg in SCREENS.items():
        rem = available_count(sno)
        print(f"  Screen {sno} ({cfg['movie']}): {rem}/{cfg['total']} seats available")

# ── Return Dictionary ──────────────────────────────────────────────────────────
def return_dictionary():
    print("\n" + "=" * 54)
    print("  BOOKINGS DICTIONARY")
    print("=" * 54)
    if not bookings:
        print("  (empty)")
    for tid, data in bookings.items():
        print(f"\n  {tid}:")
        for k, v in data.items():
            if isinstance(v, dict) and v:
                print(f"      {k}:")
                for ck, cv in v.items():
                    print(f"          {ck:<18}: {cv}")
            elif isinstance(v, list):
                print(f"      {k:<20}: {', '.join(map(str, v))}")
            else:
                print(f"      {k:<20}: {v}")
    print("\n" + "=" * 54)
    return bookings


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "=" * 54)
    print("       CineBook -- Movie Ticket Booking System")
    print("=" * 54)

    while True:
        print("\n" + "=" * 54)
        print("  MAIN MENU")
        print("  [1]  Book Tickets")
        print("  [2]  Cancel Tickets")
        print("  [3]  View Remaining Seats")
        print("  [not interested]  Exit")
        print("=" * 54)

        choice = input("\n  Your choice: ").strip()

        # ── Exit ───────────────────────────────────────────────────────────────
        if choice.lower() == "not interested":
            print("\n  Thank you for using CineBook. Goodbye!")
            break

        # ── Book ───────────────────────────────────────────────────────────────
        elif choice == "1":
            print("\n  -- New Booking --")
            name = input("  Name          : ").strip()
            if not name:
                print("  [!] Name cannot be empty.")
                continue

            mobile = input("  Mobile Number : ").strip()
            if not mobile.isdigit() or len(mobile) < 10:
                print("  [!] Enter a valid 10-digit mobile number.")
                continue

            date = input("  Show Date (DD-MM-YYYY): ").strip()
            if not date:
                print("  [!] Date cannot be empty.")
                continue

            print("\n  Select Movie:")
            for sno, cfg in SCREENS.items():
                avail = available_count(sno)
                print(f"  [{sno}]  {cfg['movie']:<28}  Rs{cfg['price']}  |  {avail} seats left")

            movie_choice = input("\n  Your choice [1/2]: ").strip()

            if movie_choice not in ("1", "2"):
                print("  [!] Invalid choice. Enter 1 or 2.")
                continue

            screen_no = int(movie_choice)
            book_seats(name, mobile, date, screen_no)

        # ── Cancel ─────────────────────────────────────────────────────────────
        elif choice == "2":
            cancel_booking()

        # ── View All ───────────────────────────────────────────────────────────
        elif choice == "3":
            remaining_seats_summary()
            for sno in SCREENS:
                display_seats(sno)

        else:
            print("  [!] Invalid option. Please choose from the menu.")

    # ── Exit Summary ───────────────────────────────────────────────────────────
    view_all_bookings()
    remaining_seats_summary()
    return return_dictionary()


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = main()
    # `result` holds the full bookings dictionary
