

class Market(self):
  def __init__(self, PublicKey, PrivateKey):
    self.PublicKey = PublicKey
    self.PrivateKey = PrivateKey
  
  # BUY HEDGECOIN LOGIC
  def buy(self,portfolio,hgc_in_circulation,user_address): # Might need some CLEANING up.
    """Main function orchestrating the buying of hgc"""
    # Did btc arrrive in account
    balance = check_money_in_bank(3)
    # What are we gonna buy with the available btc?
    number_of_coins = len(portfolio)

    open_orders = []
    i=0

    # Chech number of coins BEFORE buy
    coins_before_buy = calculate_holdings(portfolio)

    # Place order for each coin in the portfolio
    for coin in portfolio:
      if i<(number_of_coins -1):
        order_id = open_order(balance/number_of_coins,portfolio[coin])
        open_orders.append(order_id)
        i+=1

      else:
        # Check remainder in btc account and place order using this remainder
        balance = check_money_in_bank(3)
        order_id = open_order(balance,portfolio[coin])
        open_orders.append(order_id)

    # Check number of coins AFTER buy
    if check_open_orders(open_orders):
      coins_after_buy = calculate_holdings(portfolio)
      # Calculate amount of hgc and send to user
      calculate_send_hgc(coins_before_buy,coins_after_buy,portfolio,hgc_in_circulation,user_address)



  def check_money_in_bank(self,id):
    """Checks if btc arrived in Crypstsy and is spendable"""
    money_in_bank = False
    count = 0
    # Checks if balance is greater than zero
    while money_in_bank == False:
      balance = Exchange.balance(id)["data"]["available"]["{}".format(id)]
      if balance > 0:
        money_in_bank = True
      # If balance is zero, perform check every x seconds with max of y times
      else:
        while count < 15:
          time.sleep(120)
          count += 1
          if count == 15:
            return "No money in the bank. Pls check."
    return balance/100 # /100 for testing purposes. Make sure to DELETE for production



  def open_order(self,to_buy,id):
    """Makes a buy order, returns order_id"""
    i=0

    # Increasing odds the order will be excecuted rapidly buy setting the price low enough (but not too low)
    best_asks = Exchange.market_orderbook(id,10,"sell")
    obtainable = best_asks["data"]["sellorders"][i]["total"]
    while to_buy > obtainable:
      i+=1
      obtainable += best_asks["data"]["sellorders"][i]["total"]
    price = best_asks["data"]["sellorders"][i]["price"]
    quantity = to_buy/price

    # Making order
    order_id = Exchange.order_create(id,quantity,"buy",price)["data"]["orderid"]
    # >>> insert further error assertions etc here
    return order_id



  # AWAITING REPLY from Cryptsy API team
  def check_open_orders(self,open_orders):
    """Check if all orders are excecuted, returns True when ok"""
    if Exchange.order(open_orders[0])["data"]["orderinfo"]["active"] != False:
  #  for order in open_orders:
  #    while Exchange.order(order)["data"]["orderinfo"]["active"] != False:
  #      time.sleep(10)
      return True



  def calculate_holdings(self,portfolio):
    """Calculates portfolio worth in btc"""
    balances = Exchange.balances()
    portfolio_balance = {}
    for coin in portfolio:
      portfolio_balance[coin]= balances["data"]["available"]["{}".format(coin)]

    return portfolio_balance



  def calculate_send_hgc(self,coins_before_buy,coins_after_buy,portfolio,hgc_in_circulation,user_address):
    """Calculates amount of Hedgecoin to send and sends it (Research needed....)"""
    # Calculate added value
    btc_value_before_buy = calculate_btc_value_portfolio(coins_before_buy,portfolio)
    btc_value_after_buy = calculate_btc_value_portfolio(coins_after_buy,portfolio)
    added_btc_value = btc_value_after_buy - btc_value_before_buy

    # Hgc/btc calculation
    hgc_per_btc = hgc_in_circulation/btc_value_before_buy

    # New hgc to issue to user
    hgc_to_send = added_btc_value * hgc_per_btc

    # Communication with ethereum contract goes here
    print "User will get ",hgc_to_send," hgc in his account with number: ",user_address



  # Needs clean up >>> passing along portfolio to find out which market a coin is traded on. Ideally portfolio should evolve from a {coin1:market1,coin2:market2} to something like {coin1:[amount1,market1]}
  def calculate_btc_value_portfolio(self,coins,portfolio):
    """Calculates the btc value of all coins in a portfolio"""
    balances = Exchange.balances()
    btc_value = 0
    for coin in coins:
      market = portfolio[coin]
      price = Exchange.market_orderbook(market,1,"buy")["data"]["buyorders"][0]["price"]
      amount = balances["data"]["available"]["{}".format(coin)]
      btc_value += price*amount
    return btc_value

  # BUY HEDGECOIN LOGIC
  def sell(self,portfolio,hgc_in_circulation,user_address):
    # sell method goes here
  




