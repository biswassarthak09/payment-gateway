from enum import Enum

class TransactionClass(Enum):
    ECOM = (1, "ecom")
    RECCURRING  = (2, "reccurring")
    MOTO = (3, "moto")

    @classmethod
    def get_value(cls, identifier):
        for item in cls:
            if item.value[0] == identifier or item.value[1] == identifier:
                return item.value[1]
        raise ValueError(f"{identifier} is not a valid {cls.__name__}")

class TransactionType(Enum):
    SALE = (1, "sale")
    AUTH = (2, "auth")
    CAPTURE = (3, "capture")
    REFUND = (4, "refund")
    VOID = (5, "void")
    REGISTER = (6, "register")

    @classmethod
    def get_value(cls, identifier):
        for item in cls:
            if item.value[0] == identifier or item.value[1] == identifier:
                return item.value[1]
        raise ValueError(f"{identifier} is not a valid {cls.__name__}")
    

class TransactionStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"
    DECLINED = "DECLINED"
    ERROR = "ERROR"
    VOID = "VOID"
    EXPIRED = "EXPIRED"

class PaymentMethod(Enum):
    CARD = "CARD"
    QR_CODE = "QR_CODE"
    WALLET = "WALLET"