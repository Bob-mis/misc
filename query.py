import requests

address = "0x7Ce3c34b2c528330A2312B6621015D58B6FbCB61"
url = f"https://eth-sepolia.blockscout.com/api/v2/addresses/{address}/transactions"

print("正在从区块链获取数据...")
try:
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        
        # 1. 账户类型
        is_contract = data.get('is_contract', False)
        print(f"1. 账户类型: {'contract' if is_contract else 'eoa'}")
        
        # 2. 寻找最早转入的水龙头
        received = [tx for tx in items if tx.get('to', {}).get('hash', '').lower() == address.lower()]
        if received:
            received.sort(key=lambda x: int(x['block']))
            from_addr = received[0].get('from', {}).get('hash', '')
            print(f"2. 最早转入来自: {from_addr}")
            if "google" in from_addr.lower() or "cloud" in from_addr.lower():
                print("   -> 水龙头标识: google")
        
        # 3. 寻找发出的最后一笔交易，计算 nonce
        sent = [tx for tx in items if tx.get('from', {}).get('hash', '').lower() == address.lower()]
        if sent:
            sent.sort(key=lambda x: int(x['block']))
            last_nonce = int(sent[-1]['nonce'])
            print(f"3. 最后一笔发出交易 nonce: {last_nonce}")
            print(f"   -> 下一笔应使用的 nonce: {last_nonce + 1}")
        
        # 4. 寻找创建的合约地址
        creations = [tx for tx in items if tx.get('to') is None and tx.get('from', {}).get('hash', '').lower() == address.lower()]
        if creations:
            contract_addr = creations[0].get('created_contract', {}).get('hash', '')
            print(f"4. 合约地址后8位: {contract_addr[-8:]}")
            
    else:
        print(f"请求失败，状态码: {response.status_code}")
except Exception as e:
    print(f"发生错误: {e}")
