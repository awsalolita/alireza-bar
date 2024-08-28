# subscription filter
* this is the payload
```
{
  "customer_id": "customer02",
  "distance": 10,
  "coupon"  : "3423-discount-01",
  "timestamp": "1595877319",
  "cost"    : 32.90,
  "return_area_id": "123"
}
```
* if it contains `coupon` route the notification to the subsctiption
```json
{
   "coupon": [{"exists": true}]
}
```
* when publishing give `message attributes`