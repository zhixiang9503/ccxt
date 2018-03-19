# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.liqui import liqui
import math


class tidex (liqui):

    def describe(self):
        return self.deep_extend(super(tidex, self).describe(), {
            'id': 'tidex',
            'name': 'Tidex',
            'countries': 'UK',
            'rateLimit': 2000,
            'version': '3',
            'has': {
                # 'CORS': False,
                # 'fetchTickers': True
                'fetchCurrencies': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/30781780-03149dc4-a12e-11e7-82bb-313b269d24d4.jpg',
                'api': {
                    'web': 'https://web.tidex.com/api',
                    'public': 'https://api.tidex.com/api/3',
                    'private': 'https://api.tidex.com/tapi',
                },
                'www': 'https://tidex.com',
                'doc': 'https://tidex.com/exchange/public-api',
                'fees': [
                    'https://tidex.com/exchange/assets-spec',
                    'https://tidex.com/exchange/pairs-spec',
                ],
            },
            'api': {
                'private': {
                    'post': [
                        'getInfoExt',
                        'getInfo',
                        'Trade',
                        'ActiveOrders',
                        'OrderInfo',
                        'CancelOrder',
                        'TradeHistory',
                        'CoinDepositAddress',
                        'WithdrawCoin',
                        'CreateCoupon',
                        'RedeemCoupon',
                    ],
                },
                'web': {
                    'get': [
                        'currency',
                        'pairs',
                        'tickers',
                        'orders',
                        'ordershistory',
                        'trade-data',
                        'trade-data/{id}',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.1 / 100,
                    'maker': 0.1 / 100,
                },
            },
            'commonCurrencies': {
                'MGO': 'WMGO',
                'EMGO': 'MGO',
            },
        })

<<<<<<< HEAD
    async def fetch_balance(self, params={}):
            await self.load_markets()
            response = await self.privatePostGetInfoExt()
            balances = response['return']
            result = {'info': balances}
            funds = balances['funds']
            currencies = list(funds.keys())
            for c in range(0, len(currencies)):
                currency = currencies[c]
                uppercase = currency.upper()
                uppercase = self.common_currency_code(uppercase)
                free = funds[currency]['value']
                used = funds[currency]['inOrders']
                total = free + used
                account = {
                    'free': free,
                    'used': used,
                    'total': total,
                }
                result[uppercase] = account
            return self.parse_balance(result)

    def common_currency_code(self, currency):
        if not self.substituteCommonCurrencyCodes:
            return currency
        if currency == 'XBT':
            return 'BTC'
        if currency == 'BCC':
            return 'BCH'
        if currency == 'DRK':
            return 'DASH'
        # they misspell DASH as DSH?(may not be True)
        if currency == 'DSH':
            return 'DASH'
        # their MGO stands for MGO on WAVES(aka WMGO), see issue  #1487
        if currency == 'MGO':
            return 'WMGO'
        # the MGO on ETH is called EMGO on Tidex
        if currency == 'EMGO':
            return 'MGO'
        return currency

=======
>>>>>>> upstream/master
    async def fetch_currencies(self, params={}):
        currencies = await self.webGetCurrency(params)
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = currency['symbol']
            precision = currency['amountPoint']
            code = self.common_currency_code(id)
            active = currency['visible'] is True
            status = 'ok'
            if not active:
                status = 'disabled'
            canWithdraw = currency['withdrawEnable'] is True
            canDeposit = currency['depositEnable'] is True
            if not canWithdraw or not canDeposit:
                active = False
            result[code] = {
                'id': id,
                'code': code,
                'name': currency['name'],
                'active': active,
                'status': status,
                'precision': precision,
                'funding': {
                    'withdraw': {
                        'active': canWithdraw,
                        'fee': currency['withdrawFee'],
                    },
                    'deposit': {
                        'active': canDeposit,
                        'fee': 0.0,
                    },
                },
                'limits': {
                    'amount': {
                        'min': None,
                        'max': math.pow(10, precision),
                    },
                    'price': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': currency['withdrawMinAmout'],
                        'max': None,
                    },
                    'deposit': {
                        'min': currency['depositMinAmount'],
                        'max': None,
                    },
                },
                'info': currency,
            }
        return result

    def get_version_string(self):
        return ''
