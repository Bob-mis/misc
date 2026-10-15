import requests

address = "0x7Ce3c34b2c528330A2312B6621015D58B6FbCB61"
start_block = 9422173
end_block = 9459169

# 使用 Etherscan 的 API (不需要 key，用免费额度)
# 注意：这里直接调用 API，让它返回指定区块范围内的交易
url = f"https://api-sepolia.etherscan.io/api?module=account&action=txlist&address={address}&startblock={start_block}&endblock={end_block}&sort=desc&apikey=YourApiKeyToken"

print("正在查询指定区间内的交易...")
try:
    response = requests.get(url, timeout=30)
    data = response.json()
    if data['status'] == '1':
        txs = data['result']
        print(f"在区间 {start_block} 到 {end_block} 内找到了 {len(txs)} 笔交易。")
        
        # 因为 sort=desc，第一笔就是最新的
        if txs:
            last_tx = txs[0]
            print(f"\n--- 区间内最后一笔交易 ---")
            print(f"区块: {last_tx['blockNumber']}")
            print(f"Nonce: {last_tx['nonce']}")
            print(f"From: {last_tx['from']}")
            print(f"To: {last_tx['to']}")
            print(f"合约地址后8位 (如果是创建交易): {last_tx['contractAddress'][-8:] if last_tx['contractAddress'] else 'N/A'}")
            
            # 计算下一笔 Nonce
            print(f"\n-> 下一笔应使用的 Nonce: {int(last_tx['nonce']) + 1}")
            
            # 顺便看下最早的一笔 (用于确认水龙头)
            print("\n--- 区间内最早一笔交易 ---")
            first_tx = txs[-1]
            print(f"From: {first_tx['from']}")
            
        else:
            print("区间内没有交易！")
    else:
        print(f"查询失败: {data['message']}")
except Exception as e:
    print(f"发生错误: {e}")
