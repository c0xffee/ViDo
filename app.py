import random
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from macCaculate import CheckMacValueService


app = Flask(__name__)


def calculate_check_mac_value(params):
    """根據 ECPay 的規範計算 CheckMacValue"""
    hash_key = 'pwFHCqoQZGmho4w6'
    hash_iv = 'EkRm7iFT261dpevs'
    method = 'sha256'  # 或 'md5'

    check_mac_service = CheckMacValueService(hash_key, hash_iv, method)
    check_mac_value = check_mac_service.generate(params)

    return check_mac_value


@app.route('/', methods=['GET', 'POST'])
def payment_form():
    TradeNo = "EKWA" + str(random.random()).split(".")[-1]
    TradeDate = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    return render_template('payment_form.html', TradeNo=TradeNo, TradeDate=TradeDate, check_mac_value='', total_amount='', choose_payment='', remark='', sponsor_name='')


@app.route('/process_non_hidden_data', methods=['POST'])
def process_non_hidden_data():
    # 處理 JavaScript 發送的非 hidden 欄位
    data = request.json
    sponsor_name = data.get('CustomField1')
    total_amount = data.get('TotalAmount')
    payment_method = data.get('ChoosePayment')
    remark = data.get('Remark')
    print(data)

    # 處理資料並回傳
    return jsonify({
        "message": "Non-hidden data received",
        "sponsor_name": sponsor_name,
        "total_amount": total_amount,
        "payment_method": payment_method,
        "remark": remark
    })


@app.route('/calculate_check_mac_value', methods=['POST'])
def calculate_check_mac_value_route():
    # 從前端接收的參數
    data = request.json

    # 準備計算 CheckMacValue 的參數
    params = {
        'MerchantID': data.get('MerchantID'),
        'MerchantTradeNo': data.get('MerchantTradeNo'),
        'MerchantTradeDate': data.get('MerchantTradeDate'),
        'PaymentType': 'aio',
        'TotalAmount': data.get('TotalAmount'),
        'TradeDesc': data.get('TradeDesc'),
        'ItemName': data.get('ItemName'),
        'ReturnURL': data.get('ReturnURL'),
        'ChoosePayment': data.get('ChoosePayment'),
        'ClientBackURL': data.get('ClientBackURL'),
        'Remark': data.get('Remark'),
        'EncryptType': '1',
        'BindingCard': data.get('BindingCard'),
        'MerchantMemberID': data.get('MerchantMemberID'),
        'CustomField1': data.get('CustomField1')
    }

    # 計算 CheckMacValue
    check_mac_value = calculate_check_mac_value(params)
    
    # 返回計算結果
    return jsonify({'CheckMacValue': check_mac_value})


if __name__ == '__main__':
    app.run(debug=True)
