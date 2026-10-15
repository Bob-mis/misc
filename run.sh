#!/bin/bash
ADDRESS="0x7Ce3c34b2c528330A2312B6621015D58B6FbCB61"
START=9422173
END=9459169

echo "===== 正在查询区间内的交易 (使用 Etherscan V2 接口) ====="
# 关键修复：加上了 chainid=11155111 (Sepolia)
curl -s "https://api.etherscan.io/v2/api?chainid=11155111&module=account&action=txlist&address=${ADDRESS}&startblock=${START}&endblock=${END}&sort=asc&apikey=YourApiKeyToken" > result.json

if grep -q '"status":"1"' result.json; then
    echo "查询成功！以下为区间内该地址的交易列表（按时间顺序）："
    python3 -c "
import json
with open('result.json') as f:
    data = json.load(f)
for tx in data['result']:
    # 只打印目标地址发出的交易，方便你数 Nonce
    if tx['from'].lower() == '0x7Ce3c34b2c528330A2312B6621015D58B6FbCB61'.lower():
        print(f\"区块: {tx['blockNumber']} | Nonce: {tx['nonce']} | To: {tx['to']} | 创建合约: {tx['contractAddress']}\")
"
else
    echo "查询失败，返回内容："
    cat result.json
fi
