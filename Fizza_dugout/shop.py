"""A tea shop API."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Tea Shop")

PRICES = {
    "chai": 80,
    "coffee": 150,
    "paratha": 120,
}

orders = {}

class OrderIn(BaseModel):
    """The shape of the JSON body that POST /orders expects."""

    item: str = Field(min_length=1)
    qty: int = Field(ge=1, le=20)
    table: int

@app.get("/hello")
def hello():
    """Say that the shop is open."""
    return {"shop": "open", "items": len(PRICES)}

@app.get("/greet")
def greet(name: str = "friend", loud: bool = False):
    """Greet somebody by name."""
    message = f"Welcome, {name}"
    if loud:
        message = message.upper()
    return {"message": message}

@app.get("/price/{item}")
def price(item: str):
    """Return the price of one item, or 404."""
    if item not in PRICES:
        raise HTTPException(status_code=404, detail=f"We do not sell {item}")
    return {"item": item, "price": PRICES[item]}


@app.post("/orders", status_code=201)
def place_order(order: OrderIn):
    """Take an order. 201 if successful, 404 if item is unavailable."""

    if order.item not in PRICES:
        raise HTTPException(
            status_code=404,
            detail=f"We do not sell {order.item}"
        )

    order_id = len(orders) + 1
    total = PRICES[order.item] * order.qty

    orders[order_id] = {
        "order_id": order_id,
        **order.model_dump(),
        "total": total
    }

    return orders[order_id]