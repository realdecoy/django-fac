from django.conf import settings
from enum import Enum

FAC_ID = getattr(settings, "FAC_ID", None)  
FAC_PASSWORD = getattr(settings, "FAC_PASSWORD", None)
FAC_DEFAULT_CURRENCY = getattr(settings, "FAC_DEFAULT_CURRENCY", None) 
FAC_BASE_URL = getattr(settings, "FAC_BASE_URL", None)

assert FAC_ID is not None and FAC_PASSWORD is not None and FAC_DEFAULT_CURRENCY is not None and FAC_BASE_URL is not None, (
    """ WARNING: django-fac is not properly configured. In your Settings file, Please set the following properties that were recieved from First Atlantic Commerce:
    * FAC_ID
    * FAC_PASSWORD 
    * FAC_DEFAULT_CURRENCY 
    * FAC_BASE_URL 
    """
)


FAC_HEADERS_JSON = {
    "PowerTranz-PowerTranzId": FAC_ID, 
    "PowerTranz-PowerTranzPassword" : FAC_PASSWORD,
    "Content-Type" : 'application/json',
    'Accept' : 'application/json'
}

FAC_HEADERS_PLAIN_TEXT = FAC_HEADERS_JSON
FAC_HEADERS_PLAIN_TEXT['Accept'] = "text/plain"

class TransactionType(Enum):
    AUTH = 1
    SALE = 2
    CAPTURE = 3
    VOID = 4
    REFUND = 5

class ISOResponseCode(str, Enum):
    TRANS_APPROVED = '00'
    AUTH_COMPLETE = '3D0'
    AUTH_3DS_NOT_SUPPORTED = '3D1'
    AUTH_ERROR = '3D3'
    HPP_COMPLETE = 'HP0'
    TOKENIZE_COMPLETE ='TK0'
    SPI_COMPLETE = 'SP4'
    FRAUD_CHECK_COMPLETE = 'FC0'

class AuthStatus(str, Enum):
    SUCCESS = 'Y'
    ATTEMPTED = 'A'
    NOT_AUTHENTICATED = 'N'
    UNAVAILABLE = 'U'
    REJECTED = 'R'

class RequestEndpoint(str, Enum):
    AUTH = 'spi/Auth'
    SALE = 'spi/Sale'
    PAYMENT = 'spi/Payment'
    CAPTURE = 'Capture'
    VOID = 'Void'
    REFUND = 'Refund'
