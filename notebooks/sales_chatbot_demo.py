# Demo notebook to test the Sales Chatbot

from src.chatbot import SalesChatbot
from src.strategies import FlanT5Strategy

# Load sales report as text
with open("../data/sales_report.csv") as f:
    lines = f.read().splitlines()[1:]  # skip header

report_lines = []
for line in lines:
    product, sales, units = line.split(",")
    report_lines.append(f"Product: {product}, Total Sales: {sales}, Units Sold: {units}")

# Initialize chatbot
chatbot = SalesChatbot(strategy=FlanT5Strategy(), report_lines=report_lines)

# Example chat
print(chatbot.chat("Show me total sales for Phone"))
print(chatbot.chat("Show me total units for Laptop"))