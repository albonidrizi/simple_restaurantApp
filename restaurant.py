import csv

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class RestaurantApp(App):
    menu = []

    def build(self):
        with open("menu.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["productId"] = int(row["id"])
                row["price"] = float(row["price"])
                del row["id"]
                self.menu.append(row)

        self.order_items = {}
        self.total_label = Label(text='Total: $0.0', size_hint=(1, 0.3))

        # Create a box layout for the app
        layout = BoxLayout(orientation='vertical')

        # label for the restaurant menu
        menu_label = Label(text='Menu', size_hint=(1, 0.1))
        layout.add_widget(menu_label)

        # label for each item in the menu
        for item in self.menu:
            item_label = Label(
                text=f'{item["productId"]}: {item["name"]}, ${item["price"]}', size_hint=(1, 0.1))
            layout.add_widget(item_label)

            # button to add the item to the order
            add_button = Button(text='Add to Order', size_hint=(1, 0.1))
            add_button.bind(on_press=lambda event,
                            item_id=item["productId"]: self.add_to_order(item_id))
            layout.add_widget(add_button)

        # label for the total
        layout.add_widget(self.total_label)

        # Button to remove the last item added to the order
        remove_button = Button(text='Remove Last Item', size_hint=(1, 0.1))
        remove_button.bind(on_press=self.remove_last_item)
        layout.add_widget(remove_button)

        # button to clear the order
        clear_button = Button(text='Clear Order', size_hint=(1, 0.1))
        clear_button.bind(on_press=self.clear_order)
        layout.add_widget(clear_button)

        return layout

    def add_to_order(self, item_id):
        if item_id in self.order_items:
            self.order_items[item_id] += 1
        else:
            self.order_items[item_id] = 1

        # Update the order total label
        total = self.get_order_total()
        self.total_label.text = f'Total: ${total:.1f}'

    def get_order_total(self):
        total = 0
        for item_id, quantity in self.order_items.items():
            for item in self.menu:
                if item["productId"] == item_id:
                    total += quantity * item['price']
                    break
        return total

    def remove_last_item(self, event):
        if len(self.order_items) > 0:
            last_item_id = list(self.order_items.keys())[-1]
            self.order_items[last_item_id] -= 1
            if self.order_items[last_item_id] == 0:
                del self.order_items[last_item_id]
                total = self.get_order_total()
                self.total_label.text = f'Total: ${total:.1f}'

    def clear_order(self, event):
        self.order_items.clear()
        self.total_label.text = 'Total: $0.0'


if __name__ == '__main__':
    RestaurantApp().run()
