# Entities


## **CardDetail**

This object is used to store card related data. 

Corresponds to `django_fac.core.entities.CardDetail`

**Signature**: 
```python
CardDetail(card_number="xxxxxxxxxxxxxxxx", cvv2="", exp_date="MM/YY", cardholder_name="John Doe")
```
### Arguments

- `card_number` - The card number that is to be processed.
- `cvv2` - The cvv (Card Verification Value) from the back of the card to be processed.
- `exp_date` - The expiry date on the card number to be processed.
- `cardholder_name` - The name on the card that is to be processed.

---

## **TransactionDetail**

This object is used to information about the transaction.

Corresponds to `django_fac.core.entities.TransactionDetail`

**Signature**: 
```python
TransactionDetail(order_id="", amount=0.0)
```

### Arguments

- `order_id` - A **unique** value that will be used to identify the transaction
- `amount` - The cvv (Card Verification Value) from the back of the card to be processed
---