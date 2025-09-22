from chatbot import SalesChatbot

bot = SalesChatbot("data/sales_report.csv")

queries = [
    "Show me total sales for Phone",
    "Show me total units for Laptop",
    "Which product sold the most?"
]

for q in queries:
    print("Query:", q)
    print("Answer:", bot.answer_query(q))
    print("---")
