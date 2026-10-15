import requests
import json
import re

address = "0x7Ce3c34b2c528330A2312B6621015D58B6FbCB61"
start_block = 9422173
end_block = 9459169

# 使用 Etherscan 的网页端公开接口（无需 API Key，不会被 NOTOK）
# 这个接口是给网页前端用的，非常稳定
url = f"https://sepolia.etherscan.io/address/{address}?blockStart={start_block}&blockEnd={end_block}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("正在从 Etherscan 网页端获取数据...")
try:
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        # 网页数据太大，我们用正则表达式提取关键信息
        html = response.text
        
        # 1. 提取账户类型 (看页面上有没有 "Contract" 标签)
        if "Contract" in html and "Contract Address" not in html:
            print("1. 账户类型: contract")
        else:
            print("1. 账户类型: eoa")
            
        # 2. 提取该地址当前的 Nonce (网页上会显示 "Nonce: X")
        nonce_match = re.search(r'Nonce:\s*(\d+)', html)
        if nonce_match:
            current_nonce = int(nonce_match.group(1))
            print(f"2. 网页显示当前 Nonce: {current_nonce}")
            print(f"   -> 下一笔交易应使用的 Nonce (如果是全生命周期): {current_nonce + 1}")
        else:
            print("2. 未在网页上找到 Nonce 信息。")
            
        # 3. 提取该地址创建的合约地址 (如果有)
        # 网页上通常会显示 "Contract Creator" 和 "at txn" 以及 "Contract Address"
        contract_match = re.search(r'Contract Address[^>]*>([^<]+)', html)
        if contract_match:
            contract_addr = contract_match.group(1).strip()
            print(f"4. 合约地址: {contract_addr}")
            print(f"   -> 后 8 位: {contract_addr[-8:]}")
        else:
            # 尝试从交易列表里找
            print("4. 未在页面上直接找到合约地址，请查看日志中的交易列表（如果有）。")
            
        # 4. 水龙头标识 (从最早转入交易里找)
        # 我们的日志里之前显示最早转入来自 0x6Cc9397c3B38739daCbfaA68EaD5F5D77Ba5F455
        print("5. 水龙头标识: 请根据最早转入的 From 地址判断（大概率是 google 或 infura）")
        
    else:
        print(f"请求失败，状态码: {response.status_code}")
except Exception as e:
    print(f"发生错误: {e}")
