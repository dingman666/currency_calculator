# -*- coding: utf-8 -*-
from lib.wox import Wox
from calculator import CurrencyConverter
import re
import json
import sys

class CurrencyCalculatorPlugin(Wox):
    def __init__(self):
        # 检查是否有命令行参数
        if len(sys.argv) == 1:
            self.debug_run = True
        else:
            self.debug_run = False
            super().__init__()
        self.converter = CurrencyConverter()

    def query(self, query):
        if not query.strip():
            return [{
                "Title": "Currency Calculator",
                "SubTitle": "Enter amount and currencies (e.g., 100 USD to CNY, 1 BTC to USD)",
                "IcoPath": "Images\\icon.ico"
            }]

        try:
            # 基本计算器功能
            if all(c in "0123456789+-*/(). " for c in query.strip()):
                try:
                    result = eval(query)
                    return [{
                        "Title": f"{query} = {result}",
                        "SubTitle": "Basic calculation result",
                        "IcoPath": "Images\\icon.ico"
                    }]
                except:
                    pass

            # 货币转换
            match = re.match(r"(\d*\.?\d+)\s*([A-Za-z¥$€£￥]+)\s+(?:to|->)?\s*([A-Za-z¥$€£￥]+)", query.strip(), re.IGNORECASE)
            if match:
                # 构造转换格式
                conversion_text = f"{match.group(1)} {match.group(2)} to {match.group(3)}"
                result = self.converter.convert(conversion_text)
                
                if isinstance(result, str) and "error" not in result.lower():
                    return [{
                        "Title": result,
                        "SubTitle": "Currency conversion result",
                        "IcoPath": "Images\\icon.ico"
                    }]

            # 单一加密货币查询
            crypto_match = re.match(r"([A-Za-z]+)$", query.strip(), re.IGNORECASE)
            if crypto_match:
                crypto = crypto_match.group(1)
                prices = self.converter.get_crypto_price(crypto)
                if prices:
                    return [{
                        "Title": f"1 {crypto.upper()} = {value:,.2f} {curr}",
                        "SubTitle": f"Current {crypto.upper()} price",
                        "IcoPath": "Images\\icon.ico"
                    } for curr, value in prices.items()]

            return [{
                "Title": "Invalid input",
                "SubTitle": "Please use format: amount currency1 to currency2",
                "IcoPath": "Images\\icon.ico"
            }]

        except Exception as e:
            return [{
                "Title": "Error occurred",
                "SubTitle": str(e),
                "IcoPath": "Images\\icon.ico"
            }]

    def debug_query(self, query):
        results = self.query(query)
        for result in results:
            print(f"Title: {result['Title']}")
            print(f"SubTitle: {result['SubTitle']}")
            print("---")

if __name__ == "__main__":
    plugin = CurrencyCalculatorPlugin()
    
    if plugin.debug_run:
        # 测试模式
        test_queries = [
            "btc",
            "100 usd to cny",
            "1 btc to usd",
            "100+200"
        ]
        for q in test_queries:
            print(f"\nTesting query: {q}")
            plugin.debug_query(q)
    else:
        # Wox 模式
        if len(sys.argv) > 1:
            rpc_json = json.loads(sys.argv[1])
            if "method" in rpc_json and rpc_json["method"] == "query":
                if len(rpc_json["parameters"]) > 0:
                    results = plugin.query(rpc_json["parameters"][0])
                    print(json.dumps({"result": results}))