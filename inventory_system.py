"""
inventory_system.py

A simple JSON-based inventory management system.
Provides functions to add, remove, and check stock levels.
"""

import json
import logging

# Configure logging to output to console
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def add_item(stock_data, item, qty, logs=None):
    """
    Adds or updates an item's quantity in the stock data.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item.
        qty (int): The quantity to set.
        logs (list, optional): A list to append log messages to.
                             Defaults to None.
    """
    if logs is None:
        logs = []

    stock_data[item] = qty
    # This f-string is for the 'logs' list specifically.
    log_message = f"Added/Updated {item}: {qty}"
    logs.append(log_message)
    # Fix: [W1203] Use lazy % formatting for logging
    logging.info("Added/Updated %s: %s", item, qty)


def remove_item(stock_data, item):
    """
    Removes an item from the stock data.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to remove.
    """
    try:
        del stock_data[item]
        # Fix: [W1203] Use lazy % formatting
        logging.info("Removed item: %s", item)
    except KeyError:
        # Fix: [W1203] Use lazy % formatting
        logging.warning("Item '%s' not found and cannot be removed.", item)


def get_qty(stock_data, item):
    """
    Gets the quantity of a specific item from stock.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item.

    Returns:
        int: The quantity of the item, or 0 if not found.
    """
    return stock_data.get(item, 0)


def load_data(filename="inventory.json"):
    """
    Loads inventory data from a JSON file.

    Args:
        filename (str): The name of the file to load from.

    Returns:
        dict: The loaded inventory data.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fix: [W1203] Use lazy % formatting
        logging.warning("Data file '%s' not found. Starting fresh.", filename)
        return {}
    except json.JSONDecodeError:
        # Fix: [W1203] Use lazy % formatting
        logging.error("Error decoding '%s'. Starting fresh.", filename)
        return {}


def save_data(stock_data, filename="inventory.json"):
    """
    Saves inventory data to a JSON file.

    Args:
        stock_data (dict): The inventory dictionary to save.
        filename (str): The name of the file to save to.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        # Fix: [W1203] Use lazy % formatting
        logging.info("Data saved to %s", filename)
    except IOError as e:
        # Fix: [W1203] Use lazy % formatting
        logging.error("Could not save data to '%s': %s", filename, e)


def print_data(stock_data):
    """
    Prints the current stock data to the console.

    Args:
        stock_data (dict): The inventory dictionary.
    """
    print("\n--- Current Stock ---")
    if not stock_data:
        print("Inventory is empty.")
    else:
        for item, qty in stock_data.items():
            print(f"{item}: {qty}")
    print("---------------------\n")


def check_low_items(stock_data, threshold=5):
    """
    Finds items with stock quantity below a threshold.

    Args:
        stock_data (dict): The inventory dictionary.
        threshold (int): The low-stock threshold.

    Returns:
        list: A list of item names that are low in stock.
    """
    low_items = [item for item, qty in stock_data.items() if qty < threshold]
    if low_items:
        # Fix: [W1203] Use lazy % formatting
        logging.info("Low stock items (below %s): %s", threshold, low_items)
    return low_items


def main():
    """
    Main function to run the inventory management tasks.
    """
    stock_data = load_data()
    print_data(stock_data)

    add_item(stock_data, "apple", 10)
    add_item(stock_data, "banana", 5)
    add_item(stock_data, "orange", 3)  # This item is low stock

    remove_item(stock_data, "grape")  # Test non-existent item removal
    remove_item(stock_data, "apple")

    print_data(stock_data)
    _ = check_low_items(stock_data, threshold=4)

    save_data(stock_data)

    logging.info("Inventory script finished.")


if __name__ == "__main__":
    main()
