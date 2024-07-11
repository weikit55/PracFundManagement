from flask import Flask, request, jsonify
from datetime import date
from InvestmentFund import InvestmentFund

app = Flask(__name__)

funds = []

@app.route('/funds',methods=['GET'])
def retrieveFunds():
    try:
        funds = InvestmentFund.retrieve_funds()
        return jsonify([fund.to_dict() for fund in funds]), 200
    except DatabaseError as e:
        raise DatabaseError("Encountered some error to retrieve the investment funds from DB")

@app.route('/funds',methods=['POST'])
def createnewFund():
    data = request.json
    try:
        new_fund = InvestmentFund(
            fund_id=data['fund_id'],
            fund_name=data['fund_name'],
            fund_manager_name=data['fund_manager_name'],
            fund_desc=data['fund_desc'],
            fund_nav=data['fund_nav'],
            creation_date=date.fromisoformat(data['creation_date']),
            performance=data['performance']
        )
        new_fund.save_db()
        return jsonify(new_fund.to_dict()), 201
    except DatabaseError as e:
        raise DatabaseError("Error saving investment funds to DB")

@app.route('/funds/<fund_id>',methods=['GET'])
def retrieveFundById(fund_id):
    fund = InvestmentFund.retrieve_funds_by_id(fund_id)
    if fund.fund_id == fund_id:
        return jsonify(fund.to_dict()), 200
    else:
        return jsonify({'Error': 'Fund does not exist'}), 404  

@app.route('/funds/<fund_id>',methods=['PUT'])
def updateFundById(fund_id):
    data = request.json
    try:
        success = InvestmentFund.update_performance(fund_id, data['performance'])
        if success:
            return '', 204
            else:
                return jsonify({'Error': 'Fund does not exist'}), 404
    except DatabaseError as e:
        raise DatabaseError("Error updating fund performance to DB")

@app.route('/funds/<fund_id>',methods=['DELETE'])
def deleteFundById(fund_id):
    try:
        success = InvestmentFund.delete_fund(fund_id)
        if success:
            return '', 204
    except DatabaseError as e:
        raise DatabaseError("Error deleting investment fund from DB")
    