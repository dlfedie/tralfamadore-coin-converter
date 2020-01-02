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


    # the above was a change conversion project i did. below i'm going to convert it to base 12. or at least attempt..
    baseTwelveChange = float(floatNumber - intNumber)
    print('base twelve change/decimal: ', baseTwelveChange)
    stringOfDecimalFixForBaseTwelve = format(baseTwelveChange, '.2f')
    print('base twelve change/decimal: ', stringOfDecimalFixForBaseTwelve)
    # the above gets us the decimal that i'll just multiply by 12 to get our "change". yes, yes, this is a lazy way of converting it, but i currently don't feel like converting the entire thing to base 12

    # so, multiply the decimal by 12 to get our change, then by 10 to bump up a decimal place. so, 120. yes, lazy.
    decimalFixForBaseTwelve = float(stringOfDecimalFixForBaseTwelve)
    changeInBaseTwelve = 120 * decimalFixForBaseTwelve
    print('change in base 12?: ', changeInBaseTwelve)

    # looks good, now just round to nearest whole
    baseTwelveFix = format(changeInBaseTwelve, '.0f')
    print('change in base 12 after round?: ', baseTwelveFix)

    # going to just give this to totalChange now
    totalChange = int(baseTwelveFix)

    # now i'm going to just switch out the numbers below to have base change of 120. so half = 60, etc. i'll comment the previous number

    # grab those half dollars, otherwise set change to remainder
    # previous check on these was 50. for base 12, let's do 60 (half of 120)
    if totalChange >= 60:
        halfDollarCoins += 1
        print('half dollars: ', halfDollarCoins)
        remainingChangeAfterHalf = totalChange - 60
    elif totalChange < 60:
        remainingChangeAfterHalf = totalChange
        print('half dollars: ', halfDollarCoins)

    # previous check here was 25. for base 12, that's 30
    if remainingChangeAfterHalf >=30:
        quarterCoins += 1
        print('quarters: ', quarterCoins)
        remainingChangeAfterQuarter = remainingChangeAfterHalf - 30
    elif remainingChangeAfterHalf < 30:
        remainingChangeAfterQuarter = remainingChangeAfterHalf
        print('quarters: ', quarterCoins)

    
    # base 10 check is 10 here (dimes). base 12 is a 12
    if remainingChangeAfterQuarter >= 12:
        # this check is a double "dime", when you have change of 24+. base 10 value was 20 below here
        if remainingChangeAfterQuarter >=24:
            dimeCoins += 1
        dimeCoins += 1
        print('dimes: ', dimeCoins)
        # dimes and pennies are our only coins that can be more than 1 in this universe
        remainingChangeAfterDime = remainingChangeAfterQuarter - (12 * dimeCoins)
    elif remainingChangeAfterQuarter < 12:
        remainingChangeAfterDime = remainingChangeAfterQuarter
        print('dimes: ', dimeCoins)

    # base 10 check is nickels on 5. base 12 will be on 6
    if remainingChangeAfterDime >= 6:
        nickelCoins += 1
        print('nickels: ', nickelCoins)
        remainingChangeAfterNickel = remainingChangeAfterDime - 6
    elif remainingChangeAfterDime < 6:
        remainingChangeAfterNickel = remainingChangeAfterDime
        print('nickels: ', nickelCoins)

    # can have up to 4 pennies, no need to count remaining change since we should be out of coins.. SHOULD. we'll see how my math goes here..
    # good lord. will tralfamadorians have half-nickels? third-nickels?? good ol' base 12. we'll say they phased them out long ago..
    # so, base 10 we need to check up to 4 pennies. base 6, since i've decided we don't need half- or third-nickels, we'll check up to 5 pennies.
    if remainingChangeAfterNickel >= 1:
        if remainingChangeAfterNickel >= 2:
            if remainingChangeAfterNickel >= 3:
                if remainingChangeAfterNickel >= 4:
                    # these 2 lines are added in base 12
                    if remainingChangeAfterNickel >= 5:
                        pennyCoins += 1
                    pennyCoins += 1
                pennyCoins += 1
            pennyCoins += 1
        pennyCoins += 1
        print('pennies: ', pennyCoins)

    # to make it easier to visualize what i'm doing, i'll send back the converted coins, and display those as well. i'll add the totalChange variable onto the sent object
    # create an object to send back!
    coinTotal = {"numberFromClient": numberPassedInFromClient, "dollarCoins": dollarCoins, "halfDollarCoins": halfDollarCoins, "quarterCoins": quarterCoins, "dimeCoins": dimeCoins, "nickelCoins": nickelCoins, "pennyCoins": pennyCoins, "toonies": toonies, "totalChange": totalChange}
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
