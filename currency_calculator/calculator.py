import requests
from datetime import datetime, timedelta
import time

class CurrencyConverter:
    def __init__(self):
        self.last_update = None
        self.update_interval = timedelta(minutes=1)
        self.rates = {}
        self.crypto_rates = {}
        
        # 添加货币符号映射
        self.currency_symbols = {
            '$': 'USD',
            'USD': 'USD',
            '¥': 'CNY',
            '￥': 'CNY',
            'CNY': 'CNY',
            '€': 'EUR',
            'EUR': 'EUR',
            '£': 'GBP',
            'GBP': 'GBP',
            '₩': 'KRW',
            'KRW': 'KRW',
            '₪': 'ILS',
            'ILS': 'ILS',
            '₹': 'INR',
            'INR': 'INR',
            'JPY': 'JPY',
            'AUD': 'AUD',
            'CAD': 'CAD',
            'CHF': 'CHF',
            'HKD': 'HKD',
            'NZD': 'NZD'
        }
        
        # API endpoints 配置
        self.apis = {
            'coingecko': {
                'base_url': 'https://api.coingecko.com/api/v3',
                'headers': {
                    'accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0'
                }
            },
            'binance': {
                'base_url': 'https://api.binance.com/api/v3',
                'headers': {
                    'accept': 'application/json'
                }
            },
            'kucoin': {
                'base_url': 'https://api.kucoin.com/api/v1',
                'headers': {
                    'accept': 'application/json'
                }
            },
            'huobi': {
                'base_url': 'https://api.huobi.pro',
                'headers': {
                    'accept': 'application/json'
                }
            }
        }

    def normalize_currency(self, currency):
        """标准化货币代码"""
        currency = currency.upper().strip()
        return self.currency_symbols.get(currency, currency)

    def get_price_from_coingecko(self, crypto):
        """从 CoinGecko 获取价格"""
        try:
            api = self.apis['coingecko']
            search_url = f"{api['base_url']}/search?query={crypto}"
            response = requests.get(search_url, headers=api['headers'])
            if response.status_code == 200:
                data = response.json()
                if data['coins']:
                    coin_id = data['coins'][0]['id']
                    price_url = f"{api['base_url']}/simple/price?ids={coin_id}&vs_currencies=usd"
                    price_response = requests.get(price_url, headers=api['headers'])
                    if price_response.status_code == 200:
                        price_data = price_response.json()
                        if coin_id in price_data:
                            return price_data[coin_id]['usd']
        except:
            pass
        return None

    def get_price_from_binance(self, crypto):
        """从 Binance 获取价格"""
        try:
            api = self.apis['binance']
            symbol = f"{crypto}USDT"
            url = f"{api['base_url']}/ticker/price?symbol={symbol}"
            response = requests.get(url, headers=api['headers'])
            if response.status_code == 200:
                data = response.json()
                if 'price' in data:
                    return float(data['price'])
        except:
            pass
        return None

    def get_price_from_kucoin(self, crypto):
        """从 KuCoin 获取价格"""
        try:
            api = self.apis['kucoin']
            symbol = f"{crypto}-USDT"
            url = f"{api['base_url']}/market/orderbook/level1?symbol={symbol}"
            response = requests.get(url, headers=api['headers'])
            if response.status_code == 200:
                data = response.json()
                if data['data']['price']:
                    return float(data['data']['price'])
        except:
            pass
        return None

    def get_price_from_huobi(self, crypto):
        """从 Huobi 获取价格"""
        try:
            api = self.apis['huobi']
            symbol = f"{crypto.lower()}usdt"
            url = f"{api['base_url']}/market/detail/merged?symbol={symbol}"
            response = requests.get(url, headers=api['headers'])
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'ok':
                    return float(data['tick']['close'])
        except:
            pass
        return None

    def get_crypto_price(self, crypto):
        """获取加密货币价格"""
        try:
            crypto = crypto.upper()
            self.update_rates()

            if crypto in self.crypto_rates:
                return {
                    'USD': self.crypto_rates[crypto]['usd'],
                    'EUR': self.crypto_rates[crypto]['usd'] * self.rates.get('EUR', 0.85),
                    'CNY': self.crypto_rates[crypto]['usd'] * self.rates.get('CNY', 6.5)
                }

            price = None
            
            # 尝试所有API获取价格
            for get_price_func in [
                self.get_price_from_coingecko,
                self.get_price_from_binance,
                self.get_price_from_kucoin,
                self.get_price_from_huobi
            ]:
                price = get_price_func(crypto)
                if price:
                    self.cache_price(crypto, price)
                    return self.format_price_response(price)

            return None

        except Exception as e:
            print(f"Error in get_crypto_price: {e}")
            return None

    def cache_price(self, crypto, price):
        """缓存价格数据"""
        self.crypto_rates[crypto] = {
            'id': crypto.lower(),
            'name': crypto,
            'usd': price
        }

    def format_price_response(self, price):
        """格式化价格响应"""
        return {
            'USD': price,
            'EUR': price * self.rates.get('EUR', 0.85),
            'CNY': price * self.rates.get('CNY', 6.5)
        }

    def update_rates(self):
        """更新法定货币汇率"""
        if (not self.last_update or 
            datetime.now() - self.last_update > self.update_interval):
            try:
                response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
                if response.status_code == 200:
                    self.rates = response.json()['rates']
                self.last_update = datetime.now()
            except Exception as e:
                print(f"Error updating rates: {e}")

    def convert(self, text):
        """Main conversion method"""
        try:
            # 标准化输入格式
            text = text.strip()
            if text.lower().startswith('cx'):
                text = text[2:].strip()
                
            # 分割输入
            parts = text.split('to')
            if len(parts) != 2:
                return "Invalid format. Please use: [amount] [currency1] to [currency2]"
                
            # 处理第一部分(金额和源币种)
            first_part = parts[0].strip().split()
            if len(first_part) != 2:
                return "Invalid amount format"
                
            try:
                amount = float(first_part[0])
                from_currency = self.normalize_currency(first_part[1])
            except ValueError:
                return "Invalid amount"
                
            # 处理目标币种
            to_currency = self.normalize_currency(parts[1].strip())
            
            # 检查是否为法定货币
            self.update_rates()
            
            # 法定货币到法定货币
            if from_currency in self.rates and to_currency in self.rates:
                result = amount * (self.rates[to_currency] / self.rates[from_currency])
                return f"{amount} {from_currency} = {result:.2f} {to_currency}"
                
            # 加密货币相关转换
            from_prices = None
            if from_currency not in self.rates:
                from_prices = self.get_crypto_price(from_currency)
                if not from_prices:
                    return f"Could not get price for {from_currency}"
                    
            to_prices = None
            if to_currency not in self.rates:
                to_prices = self.get_crypto_price(to_currency)
                if not to_prices:
                    return f"Could not get price for {to_currency}"
                    
            # 加密货币到法定货币
            if from_prices and to_currency in ['USD', 'EUR', 'CNY']:
                result = amount * from_prices[to_currency]
                return f"{amount} {from_currency} = {result:.2f} {to_currency}"
                
            # 法定货币到加密货币
            if from_currency in ['USD', 'EUR', 'CNY'] and to_prices:
                usd_amount = amount
                if from_currency != 'USD':
                    usd_amount = amount / self.rates[from_currency]
                result = usd_amount / to_prices['USD']
                return f"{amount} {from_currency} = {result:.8f} {to_currency}"
                
            # 加密货币到加密货币
            if from_prices and to_prices:
                result = amount * (from_prices['USD'] / to_prices['USD'])
                return f"{amount} {from_currency} = {result:.8f} {to_currency}"
                
            return "Could not perform conversion"
            
        except Exception as e:
            return f"Conversion error: {str(e)}"

def main():
    converter = CurrencyConverter()
    while True:
        try:
            text = input("> ")
            if text.lower() == 'q':
                break
            result = converter.convert(text)
            print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()