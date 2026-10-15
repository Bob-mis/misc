#!/bin/bash
ADDRESS="0x7Ce3c34b2c528330A2312B6621015D58B6FbCB61"
START=9422173
END=9459169

echo "===== 正在查询区间内的交易 (使用 Etherscan 公共接口) ====="
# 使用 curl 模拟浏览器访问 Etherscan 的 API (无需 key)
curl -s "https://api-sepolia.etherscan.io/api?module=account&action=txlist&address=${ADDRESS}&startblock=${START}&endblock=${END}&sort=asc&apikey=YourApiKeyToken" > result.json

# 检查是否返回了有效数据
if grep -q '"status":"1"' result.json; then
    echo "查询成功！以下为区间内的交易列表（按时间顺序）："
    # 用 python 解析 json 并打印关键信息
    python3 -c "
import json
with open('result.json') as f:
    data = json.load(f)
for tx in data['result']:
    print(f\"区块: {tx['blockNumber']} | Nonce: {tx['nonce']} | From: {tx['from']} | To: {tx['to']} | 合约创建: {tx['contractAddress']}\")
"
else
    echo "查询失败，API 返回内容如下："
    cat result.json
fi
