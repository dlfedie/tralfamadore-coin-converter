import flask
from flask import request, jsonify
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def turnToCoins(numberPassedInFromClient, type):
    # just going to declare values here and add to them if needed
    dollarCoins = 0
    halfDollarCoins = 0
    quarterCoins = 0
    dimeCoins = 0
    nickelCoins = 0
    pennyCoins = 0
    toonies = 0

    currency = type
    print('in turntocoins, type: ', currency)
    # convert the number to float if it's not already
    floatNumber = float(numberPassedInFromClient)
    
    # doing the below a better way. but saving for posterity
    # round it to 2 decimals if needed
    # roundedFloat = round(floatNumber, 2)
    # print('roundedFloat is: ', roundedFloat)
    
    # grab the int because that'll allow us to strip the decimal
    intNumber = int(floatNumber)


    # dollar coins is just going to be the int value. of course now i'm getting cute and trying Canadian currency..
    if currency == 'US':
        dollarCoins = intNumber
        print('dollars: ', dollarCoins)
    elif currency == 'Canada':
        print('are we even getting here?')
        
        if intNumber == 0:
            dollarCoins = 0
            toonies = 0
        elif intNumber == 1:
            dollarCoins = 1
        elif (intNumber % 2) == 0:
            toonies = int(intNumber / 2)
            print('toonies: ', toonies)
        elif (intNumber % 2) > 0:
            dollarCoins = 1
            toonies = int((intNumber - 1) / 2)
            print('dollars: ', dollarCoins)
            print('toonies: ', toonies)

    # much better to just split the string at . and grab our decimal places there, otherwise FLOATING POINT GETS BARFY
    # but first, only grab our 2 decimals and round them correctly
    decimalFix = format(floatNumber, '.2f')
    stringChange = decimalFix.split(".")
    print('string split1: ', stringChange[0], ' string split2: ', stringChange[1])
    # i'll just then grab the total change to be the rounded 2 decimal number
    totalChange = int(stringChange[1])
    print('totalChange: ', totalChange)

    # decimal will give us the remainders we need to deal with
    # decimal = roundedFloat - float(intNumber)
    # print('decimal:', decimal)
    # decimalFix = format(decimal, '.2f')
    # print('decimalFix:', decimalFix)
    # now to just make it all whole numbers... we'll see if this works

    # totalChange = float(decimalFix) * 100
    # print('totalChange: ', totalChange)


    # grab those half dollars, otherwise set change to 
    if totalChange >= 50:
        halfDollarCoins += 1
        print('half dollars: ', halfDollarCoins)
        remainingChangeAfterHalf = totalChange - 50
    elif totalChange < 50:
        remainingChangeAfterHalf = totalChange
        print('half dollars: ', halfDollarCoins)

    if remainingChangeAfterHalf >=25:
        quarterCoins += 1
        print('quarters: ', quarterCoins)
        remainingChangeAfterQuarter = remainingChangeAfterHalf - 25
    elif remainingChangeAfterHalf < 25:
        remainingChangeAfterQuarter = remainingChangeAfterHalf
        print('quarters: ', quarterCoins)

    if remainingChangeAfterQuarter >= 10:
        if remainingChangeAfterQuarter >=20:
            dimeCoins += 1
        dimeCoins += 1
        print('dimes: ', dimeCoins)
        # dimes and pennies are our only coins that can be more than 1 in this universe
        remainingChangeAfterDime = remainingChangeAfterQuarter - (10 * dimeCoins)
    elif remainingChangeAfterQuarter < 10:
        remainingChangeAfterDime = remainingChangeAfterQuarter
        print('dimes: ', dimeCoins)

    if remainingChangeAfterDime >= 5:
        nickelCoins += 1
        print('nickels: ', nickelCoins)
        remainingChangeAfterNickel = remainingChangeAfterDime - 5
    elif remainingChangeAfterDime < 5:
        remainingChangeAfterNickel = remainingChangeAfterDime
        print('nickels: ', nickelCoins)

    # can have up to 4 pennies, no need to count remaining change since we should be out of coins.. SHOULD. we'll see how my math goes here..
    if remainingChangeAfterNickel >= 1:
        if remainingChangeAfterNickel >= 2:
            if remainingChangeAfterNickel >= 3:
                if remainingChangeAfterNickel >= 4:
                    pennyCoins += 1
                pennyCoins += 1
            pennyCoins += 1
        pennyCoins += 1
        print('pennies: ', pennyCoins)

    # create an object to send back!
    coinTotal = {"numberFromClient": numberPassedInFromClient, "dollarCoins": dollarCoins, "halfDollarCoins": halfDollarCoins, "quarterCoins": quarterCoins, "dimeCoins": dimeCoins, "nickelCoins": nickelCoins, "pennyCoins": pennyCoins, "toonies": toonies}
    return coinTotal




@app.route('/', methods=['GET'])
def home():
    return "<h1>Hullo</h1>"

@app.route('/convert', methods=['PUT'])
def convert():
    # aha! force it to json. using args below was just using url args. that was not cutting it.
    req_data = request.get_json()

    print('reqdata maybe working now?: ', req_data)
    amountFromClient = req_data['amount']
    type = req_data['type']
    print('type is: ', type)
    # req.args only gets url args.. forgot to switch postman to actually send json, and that's why it was initially working when the client was not.
    # amountFromClient = request.args['amount']
    print('amount coming from client: ', amountFromClient)
    coinanator = turnToCoins(amountFromClient, type)
    return coinanator


port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
