import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class RestaurantOrderManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management App")
        self.root.geometry("800x600")

        # Menu items and prices in USD
        self.menu_items = {
            "FRIES MEAL": 2,
            "LUNCH MEAL": 2,
            "BURGER MEAL": 3,
            "PIZZA MEAL": 4,
            "CHEESE BURGER": 2.5,
            "DRINKS": 1,
            "Chicken Fry":1
        }

        self.exchange_rate = 82  # USD to INR

        # Background
        self.setup_background()

        # Main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Heading
        ttk.Label(
            self.main_frame,
            text="Restaurant Order Management",
            font=("Arial", 20, "bold")
        ).grid(row=0, columnspan=3, padx=10, pady=10)

        self.menu_labels = {}
        self.menu_quantities = {}

        # Menu UI
        for i, (item, price) in enumerate(self.menu_items.items(), start=1):
            label = ttk.Label(
                self.main_frame,
                text=f"{item} ($ {price}):",
                font=("Arial", 12)
            )
            label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            self.menu_labels[item] = label

            quantity_entry = ttk.Entry(self.main_frame, width=10)
            quantity_entry.grid(row=i, column=1, padx=10, pady=5)
            quantity_entry.insert(0, "0")
            self.menu_quantities[item] = quantity_entry

        # Currency selection
        self.currency_var = tk.StringVar(value='USD')
        ttk.Label(self.main_frame, text="Select Currency:", font=("Arial", 12)).grid(
            row=len(self.menu_items) + 1, column=0, padx=10, pady=5, sticky=tk.W
        )

        currency_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.currency_var,
            state="readonly",
            values=('USD', 'INR', 'BDT')
        )
        currency_dropdown.grid(row=len(self.menu_items) + 1, column=1, padx=10, pady=5)

        self.currency_var.trace('w', self.update_menu_prices)

        # Order button
        order_button = ttk.Button(
            self.main_frame,
            text="Place Order",
            command=self.place_order
        )
        order_button.grid(row=len(self.menu_items) + 2, columnspan=2, pady=20)

    def setup_background(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        try:
            img = Image.open("E:\Codingal/Module_7/Day_6/food.jpg")
            img = img.resize((800, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
        except Exception:
            self.canvas.config(bg="#f0f0f0")

    def update_menu_prices(self, *args):
        currency = self.currency_var.get()

        if currency == "INR":
            symbol = "₹"
            rate = self.exchange_rate
        elif currency == "BDT":
            symbol = "৳"
            rate = 110
        elif currency == "USD":
            symbol = "$"
            rate = 1
        else:
            symbol = "$"
            rate = 1

        for item, label in self.menu_labels.items():
            price = self.menu_items[item] * rate
            label.config(text=f"{item} ({symbol}{price:.2f}):")

    def place_order(self):
        total_cost = 0
        order_summary = "--- Order Summary ---\n"
        currency = self.currency_var.get()

        if currency == "INR":
            symbol = "₹"
            rate = self.exchange_rate
        elif currency == "BDT":
            symbol = "৳"
            rate = 110
        elif currency == "USD":
            symbol = "$"
            rate = 1
        else:
            symbol = "$"
            rate = 1

        for item, entry in self.menu_quantities.items():
            qty_str = entry.get()
            if qty_str.isdigit():
                qty = int(qty_str)
                if qty > 0:
                    item_price = self.menu_items[item] * rate
                    cost = qty * item_price
                    total_cost += cost
                    order_summary += f"{item}: {qty} x {symbol}{item_price:.2f} = {symbol}{cost:.2f}\n"

        if total_cost > 0:
            order_summary += f"\nTotal Bill: {symbol}{total_cost:.2f}"
            messagebox.showinfo("Order Placed", order_summary)
        else:
            messagebox.showwarning("Empty Order", "Please enter a quantity for at least one item.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantOrderManagement(root)
    root.mainloop()
