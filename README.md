
# Django FAC 


`django-fac` is a python package that helps to simplify the integration with First Atlantic Commerce payment gateway.

PyPi Package: https://pypi.org/project/django-fac/

Detailed documentation is in the "docs" directory.

Table of contents
=================
<!--ts-->
   * [Installation](#installation)
   * [Configurations](#configurations)
   * [Usage](#usage)
      * [Example](#example)
   * [Tests](#tests)
   * [Local Development](#local-development)
   * [API Reference](#api-reference)
<!--te-->


---

&nbsp;

## Installation

1. First we need to install the `django-fac`:
```bash
pip install django-fac
```

&nbsp;

## Configurations

2. Add "django_fac" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
    ...
    'django_fac',
]
```

3. Setting up the package config variables. It is recommemded to store the values in environment variables.

```python
FAC_ID = "..."
FAC_PASSWORD = "..."
FAC_DEFAULT_CURRENCY = "..."
FAC_BASE_URL = "https://..."

```

&nbsp;

## Usage

This is an example of how the authorization process works

### **Example**
```python
from django_fac.core import payment
from django_fac.entities import TransactionDetail, CardDetail

transaction_detail = TransactionDetail(
    order_id="1234567",
    amount=2000
)

card_detail = CardDetail(
    card_number="0000-0000-0000-000", 
    cvv2="123", 
    exp_date="09/28", # MM/YY
    cardholder_name="John Doe"
)

# This URL will recieve the status of the transaction after authorization
redirect_url = "https://your-domain.com/webhook/payment"

response = payment.authorize(transaction_detail, card_detail, redirect_url)

# TODO: add remaining logic
```

&nbsp;

## Tests

....

&nbsp;

## Local Development

If you are interested in contributing to the project then the following instructions will apply to you.

&nbsp;

## API Reference

 - [Payment](docs/api-guide/payment.md) - Read more about how the Payments API can be used.
 - [Entities](docs/api-guide/entities.md) - Read more about how the entities can be used.