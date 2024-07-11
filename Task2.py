from flask import Flask, request, jsonify
from datetime import date
from InvestmentFund import InvestmentFund

app = Flask(__name__)

funds = []

@app.route('/funds',methods=['GET'])
def retrieveFunds():
    return jsonify([fund.to_dict() for fund in funds]), 200

@app.route('/funds',methods=['POST'])
def createnewFund():
    data = request.json
    new_fund = InvestmentFund(
        fund_id=data['fund_id'],
        fund_name=data['fund_name'],
        fund_manager_name=data['fund_manager_name'],
        fund_desc=data['fund_desc'],
        fund_nav=data['fund_nav'],
        creation_date=date.fromisoformat(data['creation_date']),
        performance=data['performance']
    )
    funds.append(new_fund)
    return jsonify(new_fund.to_dict()), 201

@app.route('/funds/<fund_id>',methods=['GET'])
def retrieveFundById(fund_id):
    for fund in funds:
        if fund.fund_id == fund_id:
            return jsonify(fund.to_dict()), 200
        else:
            return jsonify({'Error': 'Fund does not exist'}), 404  

@app.route('/funds/<fund_id>',methods=['PUT'])
def updateFundById(fund_id):
    for fund in funds:
        if fund.fund_id == fund_id:
            fund.performance = request.json.get('performance',fund.performance)
            return jsonify(fund.to_dict()), 200
        else:
            return jsonify({'Error': 'Fund does not exist'}), 404

@app.route('/funds/<fund_id>',methods=['DELETE'])
def deleteFundById(fund_id):
    for fund in funds:
        if fund.fund_id == fund_id:
            funds.remove(fund)
            return '', 204