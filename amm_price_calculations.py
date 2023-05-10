import math

DEX_FEE = 0.003

def lower_profit_deviation(S):
    pass
    return S * ((1 - DEX_FEE)**2)
    
def upper_profit_deviation(S):
    pass
    return S / ((1 - DEX_FEE)**2)

def calculate_delta_X(X, k, price_new):
    return math.sqrt(k / price_new) - X

def calculate_delta_Y(Y, k, price_new):
    return math.sqrt(k * price_new) - Y

def extractable_value_in_USD(price_new, X, Y):
    k = X * Y
    delta_X =  calculate_delta_X(X, k, price_new)
    delta_Y = calculate_delta_Y(Y, k, price_new)

    if price_new < (Y/X):
        delta_X = delta_X*(1/(1-DEX_FEE))
    else:
        delta_Y = delta_Y*(1/(1-DEX_FEE))
        
    return (price_new * delta_X + delta_Y) * (-1)

def get_input_for_price_movement(X, Y, algo_price_after, trade_X_for_Y):
    k = X * Y
    if trade_X_for_Y:
        delta = calculate_delta_X(X, k, algo_price_after)
    else:
        delta = calculate_delta_Y(Y, k, algo_price_after)
    return delta * (1/(1-DEX_FEE))

def get_price_output_poolsize_of_input(X,Y, input, trade_X_for_Y):
    k = X * Y
    input_after_fees = input * (1-DEX_FEE)
    if trade_X_for_Y:
        X_new = X + input_after_fees
        Y_new = k / X_new
        output = Y - Y_new
    else:
        Y_new = Y + input_after_fees
        X_new = k / Y_new
        output = X - X_new
    price = Y_new/X_new
    return price, output, X_new, Y_new