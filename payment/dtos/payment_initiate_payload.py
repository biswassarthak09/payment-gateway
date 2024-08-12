from dataclasses import dataclass

@dataclass
class CustomerDetailsDTO:
    name : str
    email : str
    phone : str
    
@dataclass
class PaymentInitatePayload:
    profile_id: int
    tran_type: str
    tran_class: str
    cart_id: str
    cart_currency: str
    cart_amount: float
    cart_description: str
    paypage_lang: str
    customer_details: CustomerDetailsDTO
    hide_shipping: bool
    callback: str
    return_url: str
    tokenise: int
    framed: bool