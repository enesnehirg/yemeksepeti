# Orders

Example Order object:
```json
{
  "id": 23,
  "user": {
    "id": 1,
    "email": "yspt@yspt.com",
    "first_name": "Yspt",
    "last_name": "Yspt"
  },
  "restaurant": "Harika Ev Yemekleri",
  "status": "Pending",
  "orderitem_set": [
    {
      "id": 15,
      "food": {
        "id": 5,
        "category": "Ev Yemekleri",
        "name": "Pilav",
        "price": 10.0
      },
      "quantity": 3,
      "order": 23
    }
  ]
}
```

### Create order

Definition: Creates order and order items which are associated with foods.

Endpoint: `POST /api/v1/orders/`

Payload: 

```
{
  "user": <int:id>,
  "restaurant": <int:id>,
  "orderitem_set": [
    {
      "food": <int:id>,
      "quantity": <int>
    }
  ]
}
```

**Note:** All fields are required.

Sample body: 

```json
{
  "user": 1,
  "restaurant": 2,
  "orderitem_set": [
    {
      "food": 3,
      "quantity": 2
    },
    {
      "food": 4,
      "quantity": 1
    }
  ]
}
```

Response: HTTP_201_CREATED and Order object.

### Complete order

Definition: Updates the status of the order to "Completed" whose ID is given. 

Endpoint: `PATCH /api/v1/complete-order/:id/`

Response: HTTP_200_OK and Order object.

### List orders

Definition: Lists all orders.

Endpoint: `GET /api/v1/orders/`

Response: HTTP_200_OK and list of Order objects.

You can also filter orders by status field with just adding a search query parameter like this:

`GET /api/v1/orders/?search=<status>`

Possible choices: Pending, Completed
