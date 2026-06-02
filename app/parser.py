import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from schema import Transaction

load_dotenv()

llm_1 = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.0)
llm_2 = ChatGoogleGenerativeAI(model="gemini-3-flash", temperature=0.0)
llm_3 = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
llm_4 = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.0)
llm_5 = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.0)

structured_llm_1 = llm_1.with_structured_output(Transaction)
structured_llm_2 = llm_2.with_structured_output(Transaction)
structured_llm_3 = llm_3.with_structured_output(Transaction)
structured_llm_4 = llm_4.with_structured_output(Transaction)
structured_llm_5 = llm_5.with_structured_output(Transaction)

resilient_llm = structured_llm_1.with_fallbacks([structured_llm_2, structured_llm_3, structured_llm_4, structured_llm_5])

system_prompt = """
You are an expert financial extraction AI for SanchayKosh. 
Your job is to analyze raw Indian UPI and banking SMS notifications. 
Extract the core financial data accurately based on the provided schema.

Rules:
1. Strip out UPI handles from vendor names (e.g., 'Zomato@okaxis' becomes 'Zomato').
2. If the message is promotional spam, an OTP, or a generic alert, flag is_valid_transaction as False.
3. Determine if the money is entering the account (credit) or leaving (debit/expense).
4. Do not hallucinate data. If a category is unclear, default to 'Miscellaneous'.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{raw_upi_sms}")
])

extraction_chain = prompt | resilient_llm

def parse_upi_sms(raw_sms: str) -> Transaction:
    """
    Passes the raw SMS through the highly resilient LangChain pipeline.
    """
    try:
        result = extraction_chain.invoke({"raw_upi_sms": raw_sms})
        return result
    except Exception as e:
        print(f"Error parsing SMS through all models: {e}")
        return None
    
if __name__ == "__main__":
    test_string = "Paid Rs 150 to Swiggy@icici. UPI Ref: 12345. Bal: Rs 1200."
    print("Testing Parser Health...")
    print(parse_upi_sms(test_string))