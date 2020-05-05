class SmartPayout():
    def __init__(self, bills, currency):
        self.channels = bills
        self.currency = currency
        self.channels_route = []
        self.total_amount = 0
        self.credit = 0
        self.messages = []

    