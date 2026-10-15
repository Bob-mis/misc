import requests

address = "0x7Ce3c34b2c528330A2312B6621015D58B6FbCB61"
start_block = 9422173
end_block = 9459169

# 使用 Etherscan 的 API (这次用另一个不需要 Key 的公共端点)
# 注意：如果这个还不行，我们就要用 Blockscout 的原始交易数据手动过滤。
# 这里优先尝试一个更稳的公共节点接口。
url = f"https://api-sepolia.etherscan.io/api?module=account&action=txlist&address={address}&startblock={start_block}&endblock={end_block}&sort=asc&apikey=YourApiKeyToken"

print("正在查询指定区间内的交易...")
try:
    response = requests.get(url, timeout=30)
    data = response.json()
    
    if data.get('status') == '1':
        txs = data['result']
        print(f"在区间 {start_block} 到 {end_block} 内找到了 {len(txs)} 笔交易。\n")
        
        # 1. 找区间内最后一笔发出的交易 (用于计算 nonce)
        sent_txs = [tx for tx in txs if tx['from'].lower() == address.lower()]
        if sent_txs:
            last_sent = sent_txs[-1] # 列表是升序，最后一个是最大的
            last_nonce = int(last_sent['nonce'])
            print(f"--- 区间内最后一笔发出交易 ---")
            print(f"Block: {last_sent['blockNumber']}")
            print(f"Nonce: {last_nonce}")
            print(f"To: {last_sent['to']}")
            print(f"-> 下一笔应使用的 Nonce: {last_nonce + 1}")
            print("-" * 30)
        else:
            print("区间内未找到该地址发出的交易。")
            
        # 2. 找区间内最早的转入交易 (用于判断水龙头)
        received_txs = [tx for tx in txs if tx['to'].lower() == address.lower()]
        if received_txs:
            first_received = received_txs[0] # 最早的一笔
            from_addr = first_received['from']
            print(f"--- 区间内最早一笔转入 ---")
            print(f"From: {from_addr}")
            # 如果 from 包含 google 关键字，标识就是 google
            if "google" in from_addr.lower() or "cloud" in from_addr.lower():
                print("-> 水龙头标识: google")
            print("-" * 30)
            
        # 3. 找创建的合约地址
        contract_creations = [tx for tx in txs if tx['to'] == '' and tx['from'].lower() == address.lower()]
        if contract_creations:
            contract_addr = contract_creations[0]['contractAddress']
            print(f"--- 创建合约 ---")
            print(f"合约地址后8位: {contract_addr[-8:]}")
            print("-" * 30)
            
    else:
        print(f"查询失败: {data.get('message', '未知错误')}")
        print("提示: 这可能是由于网络限制或 API 限制。")
except Exception as e:
    print(f"发生错误: {e}")
