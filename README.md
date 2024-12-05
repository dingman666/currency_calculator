# Currency Calculator

一个强大的多功能货币转换计算器，支持法定货币和加密货币之间的实时转换。

## 主要特性

- 支持多种法定货币转换 (USD, EUR, CNY, GBP, JPY等)
- 支持主流加密货币转换 (BTC, ETH, USDT等)
- 实时汇率更新 (每分钟自动更新)
- 多个数据源支持:
  - CoinGecko API
  - Binance API
  - KuCoin API
  - Huobi API
- 支持货币符号识别 ($, ¥, €, £等)
- 高精度计算
  - 法定货币保留2位小数
  - 加密货币保留8位小数
- 简单易用的命令行界面

## 使用方法

基本格式:cx [金额] [源币种] to [目标币种]
示例:
cx 100 USD to CNY
100 USD = 721.50 CNY

cx 1 BTC to USD
1 BTC = 42631.85 USD

cx 1000 € to ¥
1000 EUR = 7821.32 CNY

## 支持的货币符号
- USD ($)
- CNY (¥/￥)
- EUR (€)
- GBP (£)
- KRW (₩)
- ILS (₪)
- INR (₹)
- 
搭配WOX插件使用
https://github.com/Wox-launcher/Wox/releases/download/v1.4.1196/Wox-Full-Installer.1.4.1196.exe

