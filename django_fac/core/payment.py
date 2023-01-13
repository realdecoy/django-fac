import requests
from requests.exceptions import JSONDecodeError
from .entities import (
    TransactionDetail, 
    CardDetail, 
    AuthorizeResponse, 
    PaymentResponse,
    CaptureResponse
)
from .constants import (
    FAC_BASE_URL,
    FAC_HEADERS_JSON,
    FAC_HEADERS_PLAIN_TEXT,
    TransactionType,
    RequestEndpoint,
)
from .utils import (
    generate_auth_request_body,
    generate_capture_request_body,
    generate_payment_request_body,
    generate_sale_request_body,
    generate_void_request_body,
    generate_refund_request_body
)


def authorize(transaction_detail: TransactionDetail, card_detail: CardDetail, redirect_url: str) -> AuthorizeResponse:
    
    if not transaction_detail.is_valid():
        raise ValueError(transaction_detail.error_message)

    if not card_detail.is_valid():
        raise ValueError(card_detail.error_message)

    url = FAC_BASE_URL + RequestEndpoint.AUTH
    body = generate_auth_request_body(transaction_detail, card_detail, redirect_url)

    response = requests.post(url=url, headers=FAC_HEADERS_JSON, json=body)
    status_code = response.status_code
    try:
        json_response = response.json()
    except JSONDecodeError:
        raise ValueError("Unable to decode Auth FAC response. This normally means something was incorrectly sent in the request (eg. Invalid or missing tansaction amount). Error: '{response.text}'")

    return AuthorizeResponse.from_response(json_response, status_code)


def sale(transaction_detail: TransactionDetail, card_detail: CardDetail, redirect_url: str):

    if not transaction_detail.is_valid():
        raise ValueError(transaction_detail.error_message)

    if not card_detail.is_valid():
        raise ValueError(card_detail.error_message)

    url  = FAC_BASE_URL + RequestEndpoint.SALE
    body = generate_sale_request_body(transaction_detail, card_detail, redirect_url)

    return requests.post(url=url, headers=FAC_HEADERS_JSON, json=body)


def payment(spi_token: str):
    url  = FAC_BASE_URL + RequestEndpoint.PAYMENT
    body = generate_payment_request_body(spi_token)

    response = requests.post(url=url, headers=FAC_HEADERS_PLAIN_TEXT, data=body)
    status_code = response.status_code

    try:
        json_response = response.json()
    except JSONDecodeError:
        raise ValueError(f"Unable to decode Payment FAC response. This normally means something was incorrectly sent in the request (eg. Invalid SPI Token or invalid/missing tansaction amount). Error: '{response.text}'")

    return PaymentResponse.from_response(json_response, status_code)

def capture(transaction_detail: TransactionDetail):

    if not transaction_detail.is_valid():
        raise ValueError(transaction_detail.error_message)

    url  = FAC_BASE_URL + RequestEndpoint.CAPTURE
    body = generate_capture_request_body(transaction_detail)
    response = requests.post(url=url, headers=FAC_HEADERS_JSON, json=body)
    status_code = response.status_code

    try:
        json_response = response.json()
    except JSONDecodeError:
        raise ValueError(f"Unable to decode Capture FAC response. Error: '{response.text}'")

    return CaptureResponse.from_response(json_response, status_code)


def refund(transaction_detail: TransactionDetail):

    if not transaction_detail.is_valid():
        raise ValueError(transaction_detail.error_message)

    url  = FAC_BASE_URL + RequestEndpoint.REFUND
    body = generate_refund_request_body(transaction_detail)

    return requests.post(url=url, headers=FAC_HEADERS_JSON, json=body)


def void(order_id: str):
    url  = FAC_BASE_URL + RequestEndpoint.VOID
    body = generate_void_request_body(order_id)

    return requests.post(url=url, headers=FAC_HEADERS_JSON, json=body)


def reverse(transaction):
    response = None

    if transaction.transaction_type == TransactionType.AUTH.value:
        response = void(order_id=transaction.order_id)
    elif transaction.transaction_type == TransactionType.SALE.value:
        transaction_detail = TransactionDetail(order_id=transaction.order_id, amount=transaction.total_payment)
        response = refund(transaction_detail=transaction_detail)
    
    return response
