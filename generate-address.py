import sys
def gen(coin):
    import poloniex
    import api_conf
    key = str(api_conf.key)
    secret = str(api_conf.secret)
    data = poloniex.Poloniex(key,secret)
    ret = data.generateNewAddress(coin)
    return ret



if sys.argv[0] != '':
    coin = str(sys.argv[1])
    ret = gen(coin)
    print ret
