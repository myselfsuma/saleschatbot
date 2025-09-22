from abc import ABC, abstractmethod

class QueryStrategy(ABC):
    @abstractmethod
    def handle(self, data, query):
        pass

class TotalSalesStrategy(QueryStrategy):
    def handle(self, data, query):
        product = query.split("for")[-1].strip()
        result = data[data['Product'] == product]['Total Sales'].sum()
        return f"Total sales for {product}: {result}"

class TotalUnitsStrategy(QueryStrategy):
    def handle(self, data, query):
        product = query.split("for")[-1].strip()
        result = data[data['Product'] == product]['Units Sold'].sum()
        return f"Total units sold for {product}: {result}"
