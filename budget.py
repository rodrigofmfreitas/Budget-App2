class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = list()
        self.deposits = list()
        self.withdraws = list()
        

    def __str__(self):
        title = f"{self.category:*^30}\n"
        items = ""
        total = 0

        for item in self.ledger:
            items += f"{item['description'][0:23]:23}" + f"{item['amount']:>7.2f}\n"
            total += item["amount"]

        output = title + items + "Total: " + str(total)
        return output
    
    def deposit(self, qty, description = ""):
        deposit = dict()
        deposit["amount"] = qty
        deposit["description"] = description
        self.deposits.append(deposit)
        self.ledger.append(deposit)

    def withdraw(self, qty, description = ""):
        if self.check_funds(qty):
            withdraw = dict()
            withdraw["amount"] = -qty
            withdraw["description"] = description
            self.withdraws.append(withdraw)
            self.ledger.append(withdraw)
            return True
        return False

    def transfer(self, qty, category):
        if self.check_funds(qty):
            self.withdraw(qty, f"Transfer to {category.category}")
            category.deposit(qty, f"Transfer from {self.category}")
            return True
        return False
            
    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        return balance
    
    def get_withdraws(self):
        total = 0
        for item in self.withdraws:
            total += item["amount"]
        return -total

    def check_funds(self, qty):
        return qty <= self.get_balance()

def create_spend_chart(categories):
    chart = "Percentage spent by category\n"
    total_withdraws = 0
    percentage = 100
    for item in categories:
        total_withdraws += item.get_withdraws()
    while percentage >= 0:
        chart += f"{percentage:>3}|"
        for item in categories:
            if percentage_test(percentage, item, total_withdraws):
                chart += " o "
            else:
                chart += "   "
        chart += " \n"
        percentage -= 10
    chart += "    "
    for item in categories:
        chart += "---"
    chart += "-\n    "
    maxlen = highest_length(categories)
    for i in range(maxlen):
        for item in categories:
            if len(item.category) > i:
                chart += f" {item.category[i]} "
            else:
                chart += "   "
        chart += " \n    "
    chart = chart[:-5]
    return chart

def percentage_test(percentage, item, total_withdraws):
    teste = round((item.get_withdraws() / total_withdraws), 2)
    if teste >= percentage/100:
        return True
    return False

def highest_length(categories):
    maxlen = -1
    for item in categories:
        if len(item.category) > maxlen:
            maxlen = len(item.category)
    return maxlen