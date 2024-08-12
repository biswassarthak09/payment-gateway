from .enums.transaction_enums import TransactionStatus

status_mapping = {
    'A': TransactionStatus.SUCCESS.value,
    'H': TransactionStatus.PENDING.value,
    'P': TransactionStatus.PENDING.value,
    'V': TransactionStatus.ERROR.value,
    'E': TransactionStatus.ERROR.value,
    'D': TransactionStatus.ERROR.value,
}