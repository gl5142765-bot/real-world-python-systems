import random
import time
from datetime import datetime

# ── Menu ──────────────────────────────────────────────────────────────────────
MENU = {
    "1": {"name": "Pizza",        "price": 150},
    "2": {"name": "Burger",       "price": 100},
    "3": {"name": "Pasta",        "price": 200},
    "4": {"name": "Water Bottle", "price":  20},
    "5": {"name": "Lemon Juice",  "price":  45},
}

# ── Global order dictionary ───────────────────────────────────────────────────
orders = {}          # { order_id: { item, quantity, price, status, enquiry_count, time } }
order_counter = 1    # auto-incrementing order number


# ── Helpers ───────────────────────────────────────────────────────────────────
def generate_order_id():
    global order_counter
    oid = f"ORD{order_counter:04d}"
    order_counter += 1
    return oid

def show_menu():
    print("\n" + "═" * 40)
    print("         🍽️  FOOD MENU")
    print("═" * 40)
    for key, item in MENU.items():
        print(f"  [{key}]  {item['name']:<15} ₹{item['price']}")
    print("═" * 40)
    print("  [done]  Finish ordering")
    print("  [view]  View all my orders")
    print("  Press ENTER to enquire about an order")
    print("═" * 40)

def place_order(choice, quantity, username):
    item     = MENU[choice]
    oid      = generate_order_id()
    total    = item["price"] * quantity
    eta      = random.randint(15, 25)
    orders[oid] = {
        "username":      username,
        "item":          item["name"],
        "quantity":      quantity,
        "unit_price":    item["price"],
        "total_price":   total,
        "status":        "ordered",
        "enquiry_count": 0,
        "placed_at":     datetime.now().strftime("%H:%M:%S"),
    }
    print(f"\n  ✅  Order Placed!")
    print(f"  🔖  Order Number : {oid}")
    print(f"  🛒  Item         : {item['name']}  x{quantity}")
    print(f"  💰  Total        : ₹{total}")
    print(f"  ⏱️   ETA          : {eta}–{eta+10} mins\n")
    return oid

def enquire_order():
    oid = input("  Enter Order Number (e.g. ORD0001): ").strip().upper()
    if oid not in orders:
        print(f"\n  ❌  Order '{oid}' not found.\n")
        return

    o = orders[oid]
    o["enquiry_count"] += 1
    count = o["enquiry_count"]

    if count == 1:
        o["status"] = "preparing"
        eta = random.randint(5, 15)
        print(f"\n  🍳  Order is being prepared!")
        print(f"  ⏱️   Arriving in {eta}–{eta+10} mins\n")
    else:
        o["status"] = "delivered"
        print(f"\n  🚚  Order {oid} has been Delivered! Enjoy your meal 🎉\n")

def view_all_orders(username):
    user_orders = {k: v for k, v in orders.items() if v["username"] == username}
    if not user_orders:
        print("\n  📭  No orders yet.\n")
        return

    print(f"\n  📋  Orders for {username}:")
    print("  " + "─" * 60)
    print(f"  {'Order ID':<10} {'Item':<15} {'Qty':>4} {'Total':>7}  Status")
    print("  " + "─" * 60)
    for oid, o in user_orders.items():
        print(f"  {oid:<10} {o['item']:<15} {o['quantity']:>4} "
              f"₹{o['total_price']:>5}  {o['status'].capitalize()}")
    print("  " + "─" * 60 + "\n")

def show_final_dictionary():
    print("\n" + "═" * 60)
    print("  📦  FINAL ORDER DICTIONARY")
    print("═" * 60)
    if not orders:
        print("  (no orders placed)")
    for oid, o in orders.items():
        print(f"\n  {oid}:")
        for k, v in o.items():
            print(f"      {k:<15}: {v}")
    print("\n" + "═" * 60)
    return orders


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "═" * 40)
    print("   🚀  Welcome to QuickBite Delivery!")
    print("═" * 40)
    username = input("  Enter your username: ").strip()
    if not username:
        username = "Guest"
    print(f"\n  Hello, {username}! 👋")

    while True:
        show_menu()
        raw = input(f"  [{username}] Choice / 'done' / 'view' / ENTER to enquire: ").strip()

        # ── Enquiry ──────────────────────────────────────────────────────────
        if raw == "":
            enquire_order()
            continue

        # ── Done ─────────────────────────────────────────────────────────────
        if raw.lower() == "done":
            print(f"\n  👋  Thanks for ordering, {username}! Goodbye!\n")
            break

        # ── View orders ──────────────────────────────────────────────────────
        if raw.lower() == "view":
            view_all_orders(username)
            continue

        # ── Place order ──────────────────────────────────────────────────────
        if raw not in MENU:
            print("  ⚠️   Invalid choice. Please pick a number from the menu.\n")
            continue

        try:
            qty_str = input("  Enter quantity: ").strip()
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("  ⚠️   Please enter a valid positive number for quantity.\n")
            continue

        place_order(raw, qty, username)

    # Return & print the dictionary
    return show_final_dictionary()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = main()
    # `result` holds the full orders dictionary for programmatic use
