import re
import urllib.request

from sherlock.items import Item

currency_dict = {
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'JPY': 'Japanese Yen',
    'GBP': 'British Pound Sterling',
    'CHF': 'Swiss Franc',
    'AUD': 'Australian Dollar',
    'CAD': 'Canadian Dollar',
    'SEK': 'Swedish Krona',
    'HKD': 'Hong Kong Dollar',
    'NOK': 'Norwegian Krone',
    'BTC': 'Bitcoin',
    'AED': 'United Arab Emirates Dirham',
    'ANG': 'Netherlands Antillean Guilder',
    'ARS': 'Argentine Peso',
    'BDT': 'Bangladeshi Taka',
    'BGN': 'Bulgarian Lev',
    'BHD': 'Bahraini Dinar',
    'BND': 'Brunei Dollar',
    'BOB': 'Bolivian Boliviano',
    'BRL': 'Brazilian Real',
    'BWP': 'Botswanan Pula',
    'CLP': 'Chilean Peso',
    'CNY': 'Chinese Yuan',
    'COP': 'Colombian Peso',
    'CRC': 'Costa Rican Colón',
    'CZK': 'Czech Republic Koruna',
    'DKK': 'Danish Krone',
    'DOP': 'Dominican Peso',
    'DZD': 'Algerian Dinar',
    'EEK': 'Estonian Kroon',
    'EGP': 'Egyptian Pound',
    'FJD': 'Fijian Dollar',
    'HNL': 'Honduran Lempira',
    'HRK': 'Croatian Kuna',
    'HUF': 'Hungarian Forint',
    'IDR': 'Indonesian Rupiah',
    'ILS': 'Israeli New Sheqel',
    'INR': 'Indian Rupee',
    'JMD': 'Jamaican Dollar',
    'JOD': 'Jordanian Dinar',
    'KES': 'Kenyan Shilling',
    'KRW': 'South Korean Won',
    'KWD': 'Kuwaiti Dinar',
    'KYD': 'Cayman Islands Dollar',
    'KZT': 'Kazakhstani Tenge',
    'LBP': 'Lebanese Pound',
    'LKR': 'Sri Lankan Rupee',
    'LTL': 'Lithuanian Litas',
    'LVL': 'Latvian Lats',
    'MAD': 'Moroccan Dirham',
    'MDL': 'Moldovan Leu',
    'MKD': 'Macedonian Denar',
    'MUR': 'Mauritian Rupee',
    'MVR': 'Maldivian Rufiyaa',
    'MXN': 'Mexican Peso',
    'MYR': 'Malaysian Ringgit',
    'NAD': 'Namibian Dollar',
    'NGN': 'Nigerian Naira',
    'NIO': 'Nicaraguan Córdoba',
    'NPR': 'Nepalese Rupee',
    'NZD': 'New Zealand Dollar',
    'OMR': 'Omani Rial',
    'PEN': 'Peruvian Nuevo Sol',
    'PGK': 'Papua New Guinean Kina',
    'PHP': 'Philippine Peso',
    'PKR': 'Pakistani Rupee',
    'PLN': 'Polish Zloty',
    'PYG': 'Paraguayan Guarani',
    'QAR': 'Qatari Rial',
    'RON': 'Romanian Leu',
    'RSD': 'Serbian Dinar',
    'RUB': 'Russian Ruble',
    'SAR': 'Saudi Riyal',
    'SCR': 'Seychellois Rupee',
    'SGD': 'Singapore Dollar',
    'SKK': 'Slovak Koruna',
    'SLL': 'Sierra Leonean Leone',
    'SVC': 'Salvadoran Colón',
    'THB': 'Thai Baht',
    'TND': 'Tunisian Dinar',
    'TRY': 'Turkish Lira',
    'TTD': 'Trinidad and Tobago Dollar',
    'TWD': 'New Taiwan Dollar',
    'TZS': 'Tanzanian Shilling',
    'UAH': 'Ukrainian Hryvnia',
    'UGX': 'Ugandan Shilling',
    'UYU': 'Uruguayan Peso',
    'UZS': 'Uzbekistan Som',
    'VEF': 'Venezuelan Bolívar',
    'VND': 'Vietnamese Dong',
    'XOF': 'CFA Franc BCEAO',
    'YER': 'Yemeni Rial',
    'ZAR': 'South African Rand',
    'ZMK': 'Zambian Kwacha'
}

# static $validSymbols = array(
#          '£' => 'GBP',	'$' => 'USD',	'€' => 'EUR',	'₴' => 'UAH',	'$u' => 'UYU',
#          'lek' => 'ALL',	'؋' => 'AFN',	'ƒ' => 'ANG',	'ман' => 'AZN',	'p.' => 'BYR',
#          'bz$' => 'BZD',	'$b' => 'BOB',	'km' => 'BAM',	'P' => 'BWP',	'лв' => 'BGN',
#          'r$' => 'BRL',	'៛' => 'KHR',	'¥' => 'JPY',	'₩' => 'KRW',	'₭' => 'LAK',
#          'ls' => 'LVL',	'lt' => 'LTL',	'ден' => 'MKD',	'rm' => 'MYR',	'₨' => 'NPR',
#          '₮' => 'MNT',	'mt' => 'MZN',	'c$' => 'NIO',	'₦' => 'NGN',	'kr' => 'SEK',
#          '﷼' => 'SAR',	'b/.' => 'PAB',	'gs' => 'PYG',	's/.' => 'PEN',	'₱' => 'CUP',
#          'zł' => 'PLN',	'lei' => 'RON',	'руб' => 'RUB',	'Дин' => 'RSD',	'Дин.' => 'RSD',
#          's' => 'SOS',	'r' => 'ZAR',	'nt$' => 'TWD',	'฿' => 'THB',	'tt$' => 'TTD',
#          '₤' => 'TRL',	'₴' => 'UAH',	'$u' => 'UYU',	'bs' => 'VEF',	'₫' => 'VND',
#          'z$' => 'ZWD');


def _query_google(ammount, from_currency, to_currency):

    query_str='a={VALUE}&from={FROM}&to={TO}'.format(VALUE=ammount, FROM=from_currency, TO=to_currency)

    with urllib.request.urlopen('http://www.google.com/finance/converter?%s' % query_str) as response:
        content =  response.read().decode(response.headers.get_content_charset())

    match_str = '<div id=currency_converter_result>([0-9\.]+)\s?([A-Z][A-Z][A-Z]) = <span class=bld>([0-9\.]+) ([A-Z][A-Z][A-Z])<\/span>'

    for line in content.split('\n'):
        if line.strip().startswith('<div id=currency_converter_result>'):
            g = re.match(match_str, line)

    return (g.group(1), g.group(2), g.group(3), g.group(4))


def _parse_query(query):

    m_query = re.match('([0-9\.]+)\s([a-zA-Z]+)\sto\s([a-zA-Z]+)', query)

    if m_query is None:
        return None

    _value = m_query.group(1)
    _from  = m_query.group(2).upper()
    _to    = m_query.group(3).upper()

    if _from not in currency_dict or _to not in currency_dict:
        return None

    return (_value, _from, _to)


def match_trigger(query):
    if _parse_query(query) is None:
        return False

    return True


def get_items(query):

    _value, _from, _to = _parse_query(query)

    from_ammount, from_currency, to_ammount, to_currency = _query_google(_value, _from, _to)

    result_text = '%s %s = %s %s' % (from_ammount, from_currency, to_ammount, to_currency)

    yield Item(result_text, '', arg=to_ammount)
