import requests

address = "0x7Ce3c34b2c528330A2312B6621015D58B6FbCB61"
start_block = 9422173
end_block = 9459169

print(f"正在精准查询区块 {start_block} 到 {end_block} 之间的数据...")

# 直接使用 Blockscout 的 API，根据区块范围过滤
url = f"https://eth-sepolia.blockscout.com/api/v2/addresses/{address}/transactions?filter=from&block_range={start_block}..{end_block}"

try:
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        
        print(f"共找到 {len(items)} 笔交易。")
        
        if items:
            # 取最后一笔交易 (列表可能是按时间倒序，第一笔是最新)
            # 我们先确保按区块排序
            items.sort(key=lambda x: int(x.get('block_number', 0)))
            last_tx = items[-1] # 取最新的一笔
            first_tx = items[0] # 取最早的一笔
            
            # 1. 计算 Nonce
            nonce = int(last_tx.get('nonce', 0))
            print(f"\n1. 最后一笔交易区块: {last_tx.get('block_number')}")
            print(f"2. 最后一笔交易 Nonce: {nonce}")
            print(f"3. 下一笔应使用的 Nonce: {nonce + 1}")
            
            # 2. 找创建合约的交易 (To 为 None)
            contract_txs = [tx for tx in items if tx.get('to') is None]
            if contract_txs:
                # 取最早的一笔创建合约交易
                contract_addr = contract_txs[0].get('created_contract', {}).get('hash', '')
                if contract_addr:
                    print(f"4. 创建的合约地址后8位: {contract_addr[-8:]}")
                else:
                    print("4. 未找到合约地址详情（可能API延迟）")
            else:
                print("4. 区间内未创建合约。")

            # 3. 判断水龙头标识 (看最早一笔转入)
            # 注意：这里我们查的是 From 的交易，要看转入得查 To。
            # 为了保险，我们可以再查一下转入记录，或者直接看这个列表。
            print(f"\n5. 请根据以下信息判断水龙头:")
            print(f"   最早一笔交易来自 (From): {first_tx.get('from', {}).get('hash', '')}")
            
        else:
            print("区间内没有交易。")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        
except Exception as e:
    print(f"发生错误: {e}")
