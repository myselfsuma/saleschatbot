import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from strategies import TotalSalesStrategy, TotalUnitsStrategy

class SalesChatbot:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.docs = [f"Product: {row['Product']}, Total Sales: {row['Total Sales']}, Units Sold: {row['Units Sold']}" for _, row in self.data.iterrows()]
        
        # Embeddings
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = FAISS.from_texts(self.docs, self.embedding_model)
        
        # LLM
        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
        llm_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=-1)
        self.llm = HuggingFacePipeline(pipeline=llm_pipeline)
        
        # Strategy mapping
        self.strategies = {
            "total sales": TotalSalesStrategy(),
            "total units": TotalUnitsStrategy()
        }
    
    def answer_query(self, query):
        # Use strategy if recognized
        for key in self.strategies:
            if key in query.lower():
                return self.strategies[key].handle(self.data, query)
        # Otherwise, fall back to LLM + RAG
        retrieved_docs = self.vectorstore.similarity_search(query, k=2)
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        prompt = f"Answer the following based on the context:\n{context}\nQuestion: {query}\nAnswer:"
        result = self.llm(prompt, max_length=200)[0]['generated_text']
        return result
