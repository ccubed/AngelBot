Fixer.io
========

Fixer.io provides currency exchange rate information in an API form by leveraging data that the European Central Bank puts out in CSV format. This allows me to provide you with currency conversion rates in AngelBot.

Commands
--------

currencies
    Show a list of currencies that the European Central Bank tracks and their identifier. When using functions in this module use the identifiers. IE: GBP or USD.

rates [Currency]
    Show a list of the latest exchange rates against a given base currency. By default, since the information is based on the European Central Bank, this returns exchange rates against the Euro. You can ask for any currency available in currencies however. For instance: USD or JPY.
    Ex: rates AUD - Exchange rates for the Australian Dollar

convert [amt] [currency] to [other currency]
    Convert an amount of one currency into another. This may not work in every combination. For some reason the European Central Bank doesn't store every combination. Make sure that amount is a number, it may start with a symbol. the word to must be present. It is part of the command.
    Ex: convert $125.37 USD to JPY - convert 125.37 US Dollars to Japanese Yen.