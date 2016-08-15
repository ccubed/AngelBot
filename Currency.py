import aiohttp


class Currency:

    def __init__(self, redis):
        self.apiurl = "https://api.fixer.io"
        self.currencies = {'USD': 'US Dollar',
                           'JPY': 'Japanese Yen',
                           'BGN': 'Bulgarian Lev',
                           'CZK': 'Czech Koruna',
                           'DKK': 'Danish Krone',
                           'GBP': 'Pound Sterling',
                           'HUF': 'Hungarian Forint',
                           'PLN': 'Polish Zloty',
                           'RON': 'Romanian Leu',
                           'SEK': 'Swedish Krona',
                           'CHF': 'Swiss Franc',
                           'NOK': 'Norwegian Krone',
                           'HRK': 'Croatian Kuna',
                           'RUB': 'Russian Rouble',
                           'TRY': 'Turkish Lira',
                           'AUD': 'Australian Dollar',
                           'BRL': 'Brazilian Real',
                           'CAD': 'Canadian Dollar',
                           'CNY': 'Chinese Yuan Renminbi',
                           'HKD': 'Hong Kong Dollar',
                           'IDR': 'Indonesian Rupiah',
                           'ILS': 'Israeli Shekel',
                           'INR': 'Indian Rupee',
                           'KRW': 'South Korean Won',
                           'MXN': 'Mexican Peso',
                           'MYR': 'Malaysian Ringgit',
                           'NZD': 'New Zealand Dollar',
                           'PHP': 'Philippine Peso',
                           'SGD': 'Singapore Dollar',
                           'THB': 'Thai Baht',
                           'ZAR': 'South African Rand',
                           'EUR': 'Euro'}
        self.commands = [['convert', self.convert], ['currencies', self.currencylist], ['rates', self.latest]]

    async def convert(self, message):
        """
        #convert x [currency] to [other currency base]
        """
        currency_from = " ".join(message.content.split("to")[0].split()[2:])
        currency_to = message.content.split("to")[1].strip()
        if currency_from not in self.currencies.keys() or currency_to not in self.currencies.keys():
            msgs = ["Please make sure to enter a valid currency. Valid currencies are as follows."]
            msg = await self.currencylist(message)
            msgs.append(msg)
            return msgs
        amt = message.content.split("to")[0].split()[1]
        try:
            amt = self.convertcurrency(amt)
        except ValueError:
            return "Amount to convert needs to be a number."
        async with aiohttp.ClientSession() as session:
            async with session.get(self.apiurl+"/latest", params={"base": currency_from, "symbols": currency_to}, headers={'User-Agent': 'AngelBot 2 (Python 3.5.1 AioHTTP)'}) as response:
                if response.status == 200:
                    jsd = await response.json()
                    if len(jsd['rates']) > 0:
                        conversion = amt * float(jsd['rates'][currency_to])
                        return "{} {} is {} {} based on data as of {}.".format(amt, self.currencies[currency_from], conversion, self.currencies[currency_to], jsd['date'])
                    else:
                        return "I can't convert {} to {} because Fixer.io has no currency rate information on that specific combination.".format(self.currencies[currency_from], self.currencies[currency_to])

    async def latest(self, message):
        """
        #currency [base]
        """
        if len(message.content.split()) == 2:
            base = message.content.split()[1]
        else:
            base = "GBP"
        async with aiohttp.ClientSession() as session:
            async with session.get(self.apiurl+"/latest", params={'base': base}, headers={'User-Agent': 'AngelBot 2 (Python 3.5.1 AioHTTP)'}) as response:
                if response.status == 200:
                    jsd = await response.json()
                    msg = "Conversion rates against 1 {} as of {}\n".format(self.currencies[jsd['base']], jsd['date'])
                    msg += "\n".join(["{}: {}".format(self.currencies[x], jsd['rates'][x]) for x in jsd['rates']])
                    return msg
                else:
                    return "I wasn't able to query Fixer.io for currency data from the European Central Bank right now. Please try again later."

    async def currencylist(self, message):
        return "\n".join(["{}: {}".format(x, self.currencies[x]) for x in self.currencies])

    @staticmethod
    def convertcurrency(number):
        try:
            float(number)
            return float(number)
        except ValueError:
            try:
                float(number[1:])
                return float(number[1:])
            except ValueError:
                return ValueError
