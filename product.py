class Product():
    def __init__(self):
        self.name = ''
        self.price = ''
        self.shop = ''
        self.url = ''
        self.comment = {}

    def __str__(self):
        return self.name + str(self.price) + self.shop + self.url
