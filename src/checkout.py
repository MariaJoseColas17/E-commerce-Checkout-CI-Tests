class Checkout:
    def __init__(self, tax_rate=0.18):
        self.items = []
        self.tax_rate = tax_rate
        self.subscription_discount = 0.10
        self.bundle_discount = 0.15

    def add_item(self, price: float, quantity: int = 1, is_bundle=False):
        self.items.append(
            {
                "price": price,
                "quantity": quantity,
                "is_bundle": is_bundle,
            }
        )

    def calculate_subtotal(self) -> float:
        return sum(i["price"] * i["quantity"] for i in self.items)

    def apply_bundle_discount(self, subtotal: float) -> float:
        has_bundle = any(i["is_bundle"] for i in self.items)
        if has_bundle:
            return subtotal * (1 - self.bundle_discount)
        return subtotal

    def apply_subscription_discount(self, amount: float, is_subscriber: bool) -> float:
        if is_subscriber:
            return amount * (1 - self.subscription_discount)
        return amount

    def calculate_tax(self, amount: float) -> float:
        return round(amount * self.tax_rate, 2)

    def calculate_total(self, is_subscriber: bool = False) -> float:
        subtotal = self.calculate_subtotal()
        subtotal = self.apply_bundle_discount(subtotal)
        subtotal = self.apply_subscription_discount(subtotal, is_subscriber)
        tax = self.calculate_tax(subtotal)
        total = subtotal + tax
        return round(total, 2)
