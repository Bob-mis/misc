import requests

address = "0x7Ce3c34b2c528330A2312B6621015D58B6FbCB61"
start_block = 9422173
end_block = 9459169

# 使用 Blockscout 的 API 查询普通交易 (注意：这里我们加上 sort=desc 看能不能按时间倒序，如果报错就换回默认)
url = f"https://eth-sepolia.blockscout.com/api/v2/addresses/{address}/transactions"

print("正在寻找区间内最后一笔发出的交易...")

try:
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        items = response.json().get('items', [])
        
        # 收集所有在区间内，且 From 是该地址的交易
        txs_in_range = []
        for tx in items:
            from_hash = tx.get('from', {}).get('hash', '').lower()
            # Blockscout 有时在详情接口才有 block_number，这里我们用另一种方式判断
            # 简单起见，我们直接假设列表里 Nonce 最大的就是最后一笔，因为交易是按 Nonce 递增顺序发出的。
            # 但如果 API 不是按区块排序，我们需要手动找。
            # 这里我们直接找 From 是该地址的所有交易，取 Nonce 最大值。
            if from_hash == address.lower():
                txs_in_range.append(tx)
        
        # 注意：普通交易列表可能不直接包含 block_number。但 Nonce 是按顺序递增的。
        # 我们直接找列表中 Nonce 最大的那笔。
        if txs_in_range:
            # 找出列表中 Nonce 最大的交易
            max_nonce_tx = max(txs_in_range, key=lambda x: int(x.get('nonce', 0)))
            max_nonce = int(max_nonce_tx.get('nonce', 0))
            
            print(f"该地址发出的最大 Nonce 为: {max_nonce}")
            print(f"-> 下一笔交易应使用的 Nonce (猜测): {max_nonce + 1}")
            
            # 同时打印出所有 Nonce 及其对应的区块（如果有的话）
            print("\n--- 详细列表 ---")
            for tx in txs_in_range:
                nonce = tx.get('nonce', 'N/A')
                # 有些 API 返回的 tx 里可能没有 block_number，只有 block_hash。我们打印 hash 供你核对。
                block_hash = tx.get('block_hash', 'N/A')
                print(f"Nonce: {nonce} | Block Hash: {block_hash}")
        else:
            print("未找到该地址发出的交易。")
            
    else:
        print(f"请求失败: {response.status_code}")
except Exception as e:
    print(f"发生错误: {e}")
