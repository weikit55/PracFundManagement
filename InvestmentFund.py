# This is Task1
class InvestmentFund:
    def __init__(self,fund_id,fund_name,fund_manager_name,fund_desc,fund_nav,creation_date,performance):
        self.fund_id = fund_id
        self.fund_name = fund_name
        self.fund_manager_name = fund_manager_name
        self.fund_desc = fund_desc
        self.fund_nav = fund_nav
        self.creation_date = creation_date
        self.performance = performance

    def to_dict(self):
        return {
            'fund_id': self.fund_id,
            'fund_name': self.fund_name,
            'fund_manager_name': self.fund_manager_name,
            'fund_desc': self.fund_desc,
            'fund_nav': self.fund_nav,
            'creation_date': self.creation_date.strftime('%Y-%m-%d'),
            'performance': self.performance
        }
    
    def save_db(self):
        connection = sqlite3.connect('investment_funds.db')
        conn = connection.cursor()
        conn.execute("""INSERT INTO investment_funds (fund_id,fund_name,fund_manager_name,fund_desc,fund_nav,creation_date,performance)
         VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (self.fund_id, self.fund_name, self.fund_manager_name, self.fund_desc, self.fund_nav, self.creation_date, self.performance))
        connection.commit()
        connection.close()

    def update_performance(fund_id, new_performance):
        connection = sqlite3.connect('investment_funds.db')
        conn = connection.cursor()
        conn.execute("UPDATE investment_funds SET performance = ? WHERE fund_id = ?", (new_performance, fund_id))
        connection.commit()
        connection.close()

    def retrieve_funds():
        connection = sqlite3.connect('investment_funds.db')
        conn = connection.cursor()
        conn.execute("SELECT * FROM investment_funds")
        funds_data = conn.fetchall()
        connection.close()
        funds = []
        for fund_data in funds_data:
            fund = InvestmentFund(*fund_data)
            funds.append(fund)
        return funds

    def retrieve_funds_by_id(fund_id):
        connection = sqlite3.connect('investment_funds.db')
        conn = connection.cursor()
        conn.execute('''
            SELECT * FROM investment_funds WHERE fund_id = ?
        ''', (fund_id,))
        fund_data = conn.fetchone()
        connection.close()
        if fund_data:
            return InvestmentFund(*fund_data)
        else:
            return None

    def delete_fund(fund_id):
        connection = sqlite3.connect('investment_funds.db')
        conn = connection.cursor()
        conn.execute('''
            DELETE FROM investment_funds WHERE fund_id = ?
        ''', (fund_id,))
        connection.commit()
        connection.close()