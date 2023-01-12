from django.conf import settings
from enum import Enum

FAC_ID = settings.FAC_ID    
FAC_PASSWORD = settings.FAC_PASSWORD
FAC_ACQUIRER_ID = settings.FAC_ACQUIRER_ID
FAC_DEFAULT_CURRENCY = settings.FAC_DEFAULT_CURRENCY
FAC_CURRENCY_EXPONENT = settings.FAC_CURRENCY_EXPONENT 
FAC_SIGNATURE_METHOD = settings.FAC_SIGNATURE_METHOD
FAC_TRANSACTION_CODE = settings.FAC_TRANSACTION_CODE
FAC_V2_BASE_URL = settings.FAC_V2_BASE_URL
FAC_MERCHANT_RESPONSE_URL = settings.FAC_MERCHANT_RESPONSE_URL

FAC_V2_HEADERS_JSON = {
    "PowerTranz-PowerTranzId": FAC_ID, 
    "PowerTranz-PowerTranzPassword" : FAC_PASSWORD,
    "Content-Type" : 'application/json',
    'Accept' : 'application/json'
}

FAC_V2_HEADERS_PLAIN_TEXT = FAC_V2_HEADERS_JSON
FAC_V2_HEADERS_PLAIN_TEXT['Accept'] = "text/plain"

# Flag as a single pass transaction (Authorization 
# and Capture as a single transaction). So no need 
# to manual capture the transaction
FAC_TRANSACTION_CODE_AUTO_CAPTURE = '8'
FAC_TRANSACTION_CODE_NONE = '0'

DEFAULT_CARD_TYPE = 'visa'
DEFAULT_BANK = 'ONLINE'

class ResponseStatusCodes_V2(Enum):
    SUCCESS = 200

class TransactionTypes_V2(Enum):
    AUTH = 1
    SALE = 2
    CAPTURE = 3
    VOID = 4
    REFUND = 5

class ISOResponseCodes_V2(str, Enum):
    AUTH_COMPLETE = '3D0'
    AUTH_3DS_NOT_SUPPORTED = '3D1'
    AUTH_ERROR = '3D3'
    SPI_COMPLETE = 'SP4'
    TRANS_APPROVED = '00'
    TOKENIZE_COMPLETE ='TK0'
    FRAUD_CHECK_COMPLETE = 'FC0'

class AuthStatuses_V2(str, Enum):
    SUCCESS = 'Y'
    ATTEMPTED = 'A'
    NOT_AUTHENTICATED = 'N'
    UNAVAILABLE = 'U'
    REJECTED = 'R'

class Card_Details_V2:
    def __init__(self, card_number, cvv2, exp_date, cardholder_name):
        self.card_number = card_number
        self.cvv2 = cvv2
        self.exp_date = exp_date
        self.cardholder_name = cardholder_name

class Transaction_Details_V2:
    def __init__(self, order_number, amount):
        self.order_number = order_number
        self.amount = amount
