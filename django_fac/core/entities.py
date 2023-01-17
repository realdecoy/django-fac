from .utils import format_expiry_date
from .constants import ISOResponseCode
import json

class CardDetail(object):
    def __init__(self, card_number: str, cvv2: str, exp_date: str, cardholder_name: str):
        self.card_number = card_number
        self.cvv2 = cvv2
        self.exp_date = exp_date
        self.cardholder_name = cardholder_name

    def is_valid(self):
        return self.card_number is not None and self.cvv2 is not None and self.exp_date is not None

    def error_message(self):
        return "All the card details values are required expect 'card_holder_name'."

    @property
    def formatted_exp_date(self):
        return format_expiry_date(self.exp_date)


class TransactionDetail(object):
    def __init__(self, order_id: str, amount: float):
        self.order_id = order_id
        self.amount = amount

    def is_valid(self):
        return isinstance(self.amount, (int, float)) and self.order_id is not None

    def error_message(self):
        if self.is_valid():
            return None

        error = "transaction_detail does not have all the required values."

        if isinstance(self.amount, (int, float)):
           error += " Ensure 'amount' is of type 'int' or 'float'."

        if self.order_id is None:
            error + " Ensure 'order_id' is not None or a duplicate."

        return error

"""
===========
"""

class AuthorizeResponse(object):
    def __init__(
        self, transaction_type: int, approved: bool, transaction_identifier: str, iso_response_code: str, response_message: str,  
        order_identifier: str, redirect_data: str, spi_token: str, status_code: int):
        self.transaction_type = transaction_type
        self.approved = approved
        self.transaction_identifier = transaction_identifier
        self.iso_response_code = iso_response_code
        self.response_message = response_message
        self.order_identifier =  order_identifier
        self.redirect_data = redirect_data
        self.spi_token = spi_token
        self.status_code = status_code

    @classmethod
    def from_response(cls, fac_response, status_code):
        return cls(
            fac_response["TransactionType"],
            fac_response["Approved"],
            fac_response["TransactionIdentifier"],
            fac_response["IsoResponseCode"],
            fac_response["ResponseMessage"],
            fac_response["OrderIdentifier"],
            fac_response["RedirectData"],
            fac_response["SpiToken"],
            status_code
       )

    def __str__(self) -> str:
        return f"AuthorizeResponse -> {self.order_identifier} :: {self.approved}"


class PaymentResponse(object):
    def __init__(
        self, transaction_type: int, approved: bool, transaction_identifier: str, iso_response_code: str, 
        response_message: str, order_identifier: str, total_amount: int, currency_code: str, rrn: str, 
        card_brand: str, status_code: int):

        self.transaction_type = transaction_type
        self.approved = approved
        self.transaction_identifier = transaction_identifier
        self.iso_response_code = iso_response_code
        self.response_message = response_message
        self.order_identifier =  order_identifier
        self.total_amount = total_amount
        self.currency_code = currency_code
        self.rrn = rrn
        self.card_brand = card_brand
        self.status_code = status_code


    @classmethod
    def from_response(cls, fac_response, status_code):
        return cls(
            fac_response["TransactionType"],
            fac_response["Approved"],
            fac_response["TransactionIdentifier"],
            fac_response["IsoResponseCode"],
            fac_response["ResponseMessage"],
            fac_response["OrderIdentifier"],
            fac_response["TotalAmount"],
            fac_response["CurrencyCode"],
            fac_response["RRN"],
            fac_response["CardBrand"],
            status_code
       )


class CaptureResponse(object):
    def __init__(
        self, original_trxn_identifier: str, transaction_type: int, approved: bool, transaction_identifier: str, iso_response_code: str, 
        response_message: str, order_identifier: str, total_amount: int, currency_code: str, rrn: str, status_code: int):

        self.original_trxn_identifier = original_trxn_identifier
        self.transaction_type = transaction_type
        self.approved = approved
        self.transaction_identifier = transaction_identifier
        self.iso_response_code = iso_response_code
        self.response_message = response_message
        self.order_identifier =  order_identifier
        self.total_amount = total_amount
        self.currency_code = currency_code
        self.rrn = rrn
        self.status_code = status_code


    @classmethod
    def from_response(cls, fac_response, status_code):
        return cls(
            fac_response["OriginalTrxnIdentifier"],
            fac_response["TransactionType"],
            fac_response["Approved"],
            fac_response["TransactionIdentifier"],
            fac_response["IsoResponseCode"],
            fac_response["ResponseMessage"],
            fac_response["OrderIdentifier"],
            fac_response["TotalAmount"],
            fac_response["CurrencyCode"],
            fac_response["RRN"],
            status_code
       )


"""
===========
"""

class AuthorizationRedirectError(object):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message


class ThreeDSecure(object):
    def __init__(
        self, eci, cavv, xid, authentication_status, protocol_version, fingerprint_indicator, ds_trans_id, response_code, card_holder_info):
        self.eci = eci,
        self.cavv = cavv,
        self.xid = xid,
        self.authentication_status = authentication_status,
        self.protocol_version = protocol_version,
        self.fingerprint_indicator = fingerprint_indicator,
        self.ds_trans_id = ds_trans_id,
        self.response_code = response_code,
        self.card_holder_info = card_holder_info,


class RiskManagement(object):
    def __init__(self, three_d_secure: ThreeDSecure):
        self.three_d_secure = three_d_secure


class AuthorizationRedirectResponse(object):
    def __init__(
        self, transaction_type: int, approved: bool, transaction_identifier: str, iso_response_code: str, response_message: str,  
        order_identifier: str, spi_token: str, risk_management: RiskManagement, errors: list[AuthorizationRedirectError]):
        self.transaction_type = transaction_type
        self.approved = approved
        self.transaction_identifier = transaction_identifier
        self.iso_response_code = iso_response_code
        self.response_message = response_message
        self.order_identifier =  order_identifier
        self.spi_token = spi_token
        self.errors = errors
        self.risk_management = risk_management

    @property
    def is_successful(self):
        codes = set(code.value for code in ISOResponseCode) 
        return self.iso_response_code in codes


class FACAuthorizationRedirectResponse(object):

    def __init__(self, response: AuthorizationRedirectResponse, transaction_identifiers: list[str], spi_tokens: list[str]):
        self.response = response
        self.transaction_identifiers = transaction_identifiers
        self.spi_tokens = spi_tokens

    @classmethod
    def from_response(cls, raw_response: object):
        response = raw_response["Response"]
        transaction_identifiers = raw_response["TransactionIdentifier"]
        spi_tokens = raw_response["SpiToken"]

        typed_response = FACAuthorizationRedirectResponse.map_response(response)
        # list(map(FACAuthorizationRedirectResponse.map_responses, response))
        
        return cls(typed_response, transaction_identifiers, spi_tokens)

    @staticmethod
    def map_response(raw_response):
        json_response = raw_response
        if isinstance(raw_response, str):
            json_response = json.loads(raw_response)

        return AuthorizationRedirectResponse(
            json_response["TransactionType"],
            json_response["Approved"],
            json_response["TransactionIdentifier"],
            json_response["IsoResponseCode"],
            json_response["ResponseMessage"],
            json_response["OrderIdentifier"],
            spi_token=json_response["SpiToken"],
            risk_management=json_response.get("RiskManagement", None),
            errors=list(map(FACAuthorizationRedirectResponse.map_response_rrrors, json_response.get("Errors", []))),
        )

    @staticmethod
    def map_response_rrrors(raw_response):
        return AuthorizationRedirectError(raw_response["Code"], raw_response["Message"])
