import requests
# import logging
from django.conf import settings
from enum import Enum

# Get an instance of a logger
# logger = logging.getLogger('renewal_logger')

# Retrieving the information from the Settings.py
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

FAC_V2_HEADERS_PLAIN_TEXT = {
    "PowerTranz-PowerTranzId": FAC_ID, 
    "PowerTranz-PowerTranzPassword" : FAC_PASSWORD,
    "Content-Type" : 'application/json', 
    'Accept' : 'text/plain'
}

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

def transactionAuthorize(transaction_details, card_details, redirect_url):
    endpoint = "spi/Auth"
    url = FAC_V2_BASE_URL + endpoint

    authRequestBody = generateAuthRequestBody(transaction_details, card_details, redirect_url)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_JSON, json=authRequestBody)

    return response

def transactionSale(transaction_details, card_details, redirect_url):
    endpoint = "spi/Sale"
    url = FAC_V2_BASE_URL + endpoint

    saleRequestBody = generateSaleRequestBody(transaction_details, card_details, redirect_url)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_JSON, json=saleRequestBody)

    return response

def transactionPayment(spiToken):
    endpoint = "spi/Payment"
    url = FAC_V2_BASE_URL + endpoint

    paymentRequestBody = generatePaymentRequestBody(spiToken)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_PLAIN_TEXT, data=paymentRequestBody)

    return response

def transactionCapture(transaction_details):
    endpoint = "Capture"
    url = FAC_V2_BASE_URL + endpoint

    captureRequestBody = generateCaptureRequestBody(transaction_details)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_JSON, json=captureRequestBody)

    return response

def transactionRefund(transaction_details):
    endpoint = "Refund"
    url = FAC_V2_BASE_URL + endpoint

    refundRequestBody = generateRefundRequestBody(transaction_details)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_JSON, json=refundRequestBody)

    return response

def transactionVoid(order_number):
    endpoint = "Void"
    url = FAC_V2_BASE_URL + endpoint

    voidRequestBody = generateVoidRequestBody(order_number)

    response = requests.post(url=url, headers=FAC_V2_HEADERS_JSON, json=voidRequestBody)

    return response

def transactionReverse(transaction):
    response = None
    if(transaction.transaction_type == TransactionTypes_V2.AUTH):
        response = transactionVoid(order_number=transaction.order_id)
    elif(transaction.transaction_type == TransactionTypes_V2.SALE):
        transaction_details = generateTransactionDetails_v2(order_number=transaction.order_id, amount=transaction.total_payment)
        response = transactionRefund(transaction_details=transaction_details)
    return response

def getFACV2ExpDate(exp_date):
    if exp_date:
        exp_date_split = exp_date.split('/')
        fac_exp_date = exp_date_split[1] + exp_date_split[0]
        return fac_exp_date
    return ''

def isValidResponseCodeV2(response_code):
    return response_code == ISOResponseCodes_V2.AUTH_COMPLETE.value or response_code == ISOResponseCodes_V2.AUTH_3DS_NOT_SUPPORTED.value

def isInvalidAuthComplete(three_d_secure_data):
    return three_d_secure_data.get("ResponseCode", "") == ISOResponseCodes_V2.AUTH_COMPLETE.value and (not (three_d_secure_data.get("AuthenticationStatus", "") == AuthStatuses_V2.SUCCESS.value or three_d_secure_data.get("AuthenticationStatus", "") == AuthStatuses_V2.ATTEMPTED.value))

def generateAuthRequestBody(transaction_details, card_details, redirect_url):
    return {
        "TransactionIdentifier": transaction_details.order_number,
        "TotalAmount": transaction_details.amount,
        "CurrencyCode": FAC_DEFAULT_CURRENCY,
        "ThreeDSecure": True,
        "Source": {
            "CardPan": card_details.card_number,
            "CardCvv": card_details.cvv2,
            "CardExpiration": card_details.exp_date,
            "CardholderName": card_details.cardholder_name
        },
        "OrderIdentifier": transaction_details.order_number,
        "AddressMatch": False,
        "ExtendedData": {
            "ThreeDSecure": {
                "ChallengeWindowSize": 4,
                "ChallengeIndicator": "01"
            },
            "MerchantResponseUrl": redirect_url
        },
        "BrowserInfo": {
            "JavaEnabled": False,
            "JavascriptEnabled": True
        }
    }

def generateSaleRequestBody(transaction_details, card_details, redirect_url):
    return {
        "TransactionIdentifier": transaction_details.order_number,
        "TotalAmount": transaction_details.amount,
        "CurrencyCode": FAC_DEFAULT_CURRENCY,
        "ThreeDSecure": True,
        "Source": {
            "CardPan": card_details.card_number,
            "CardCvv": card_details.cvv2,
            "CardExpiration": card_details.exp_date,
            "CardholderName": card_details.cardholder_name
        },
        "OrderIdentifier": transaction_details.order_number,
        "AddressMatch": False,
        "ExtendedData": {
            "ThreeDSecure": {
                "ChallengeWindowSize": 4,
                "ChallengeIndicator": "01"
            },
            "MerchantResponseUrl": redirect_url
        },
        "BrowserInfo": {
            "JavaEnabled": False,
            "JavascriptEnabled": True
        }
    }

def generatePaymentRequestBody(spiToken):
    return '\"' + spiToken + '\"'

def generateCaptureRequestBody(transaction_details):
    return {
        "TotalAmount": transaction_details.amount,
        "TransactionIdentifier": transaction_details.order_number
    }

def generateRefundRequestBody(transaction_details):
    return {
        "Refund": True,
        "TransactionIdentifier": transaction_details.order_number,
        "TotalAmount": transaction_details.amount,
        "CurrencyCode": FAC_DEFAULT_CURRENCY,
        "Source": {
            "CardPresent": False,
            "CardEmvFallback": False,
            "ManualEntry": False,
            "Debit": False,
            "Contactless": False,
            "CardPan": "",
            "MaskedPan": ""
        },
        "TerminalCode": "",
        "TerminalSerialNumber": "",
        "AddressMatch": False
    }

def generateVoidRequestBody(order_number):
    return {
        "TransactionIdentifier": order_number,
        "TerminalCode": "",
        "TerminalSerialNumber": "",
        "AutoReversal": False
    }

def generateCardDetails_v2(card_number, cvv2, exp_date, cardholder_name):
    card_details = Card_Details_V2(card_number=card_number, cvv2=cvv2, exp_date=exp_date, cardholder_name=cardholder_name)
    return card_details

def generateTransactionDetails_v2(order_number, amount):
    transaction_details = Transaction_Details_V2(order_number=order_number, amount=amount)
    return transaction_details