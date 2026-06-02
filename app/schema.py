from pydantic import BaseModel, Field, field_validator
from enum import Enum

class ExpenseCategory(str, Enum):
    FOOD = "Food and Dining"
    TRANSPORT = "Travel and Transportation"
    LUXURY = "Luxury and Entertainment"
    UTILITY = "Utilities and Bills"
    SHOPPING = "Shopping and Personal Care"
    HEALTH = "Health and Wellness"
    MISC = "Miscellaneous"

class Transaction(BaseModel):
    """
    Schema for extracting structured data from a raw UPI notification string.
    Langchain will force the LLM to output data in this format, which can then be easily parsed and stored in a database.
    """
    amount: float = Field(description="The exact amount of the transaction, extracted from the UPI notification string. Must be a positive number.")
    vendor: str = Field(description="The clean absolute name of the vendor or merchant payed to in the transaction, extracted from the UPI notification string.Strip away any UPI handles or bank suffixes (e.g., return 'Zomato' instead of 'Zomato@okaxis')")
    timestamp: str = Field(description="The exact timestamp of the transaction, extracted from the UPI notification string. Should be in ISO 8601 format. If the year is missing, infer the current year.")
    category: ExpenseCategory = Field(description="The category of the transaction, determined  on the vendor and other contextual information in the UPI notification string. Must be one of the predefined categories in the ExpenseCategory enum. Default to 'Miscellaneous' if the category cannot be determined.")
    is_expense: bool = Field(description="True if money was debited/spent. False if money was credited/received, extracted from the UPI notification string.")
    is_valid_transaction: bool = Field(description="True ONLY if this is a genuine financial transaction. False if it is a promotional message, OTP, or spam.")

    @field_validator('amount')
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError('Amount must be a positive number.')
        return value