prices = {"chai": 80, "coffee": 150}
 
for item in ["chai", "lassi", "coffee"]:
    try:
        price = prices[item]
    except KeyError:
        print(f"{item}: not on the menu")
    else:
        print(f"{item}: {price} rupees")
    finally:
        print(f"  (asked about {item})")
