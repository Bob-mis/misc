import requests

address = "0x7Ce3c34b2c528330A2312B6621015D58B6FbCB61"
# 使用 Blockscout 的 API，通过 URL 参数直接告诉服务器我们要什么
base_url = f"https://eth-sepolia.blockscout.com/api/v2/addresses/{address}"

print("正在从区块链获取数据...")

try:
    # 1. 获取账户基本信息 (用于判断账户类型)
    response_info = requests.get(base_url, timeout=30)
    if response_info.status_code == 200:
        data = response_info.json()
        is_contract = data.get('is_contract', False)
        print(f"1. 账户类型: {'contract' if is_contract else 'eoa'}")
    
    # 2. 获取交易列表 (让它按时间倒序排列，最新的在前面)
    txs_url = f"{base_url}/transactions?sort=desc"
    response_txs = requests.get(txs_url, timeout=30)
    
    if response_txs.status_code == 200:
        txs_data = response_txs.json()
        items = txs_data.get('items', [])
        
        print(f"\n[总计获取到 {len(items)} 笔交易]")
        
        # 筛选出该地址“发出”的交易 (计算 nonce)
        sent_txs = [tx for tx in items if tx.get('from', {}).get('hash', '').lower() == address.lower()]
        if sent_txs:
            # 因为已经按时间倒序排列，第一笔就是最新的
            last_sent = sent_txs[0]
            last_nonce = int(last_sent.get('nonce', 0))
            print(f"3. 最新一笔发出交易 nonce: {last_nonce}")
            print(f"   -> 下一笔应使用的 nonce: {last_nonce + 1}")
        else:
            print("3. 未找到发出的交易")
            
        # 筛选出该地址“创建合约”的交易 (找合约地址)
        # 创建合约的交易，它的 to 字段是空的 (None)
        create_txs = [tx for tx in items if tx.get('to') is None and tx.get('from', {}).get('hash', '').lower() == address.lower()]
        if create_txs:
            # 取最早的一笔创建合约交易（或者你题目指定的区间内）
            # 这里直接找最新的一笔 creation，因为它在列表最前面
            target_tx = create_txs[0] 
            contract_addr = target_tx.get('created_contract', {}).get('hash', '')
            if contract_addr:
                print(f"4. 合约地址后8位: {contract_addr[-8:]}")
            else:
                print("4. 找不到合约地址详情，可能未成功创建")
        else:
            print("4. 未找到创建合约的交易")
            
        # 筛选出该地址“收到”的交易 (找水龙头)
        # 因为我们需要“最早”的一笔，所以看列表的最后面
        received_txs = [tx for tx in items if tx.get('to', {}).get('hash', '').lower() == address.lower()]
        if received_txs:
            # 列表是倒序的，所以最早的一笔在最后
            first_received = received_txs[-1]
            from_addr = first_received.get('from', {}).get('hash', '')
            print(f"2. 最早转入来自地址: {from_addr}")
            # 判断是不是 Google 水龙头
            if "google" in from_addr.lower() or "cloud" in from_addr.lower():
                print("   -> 水龙头标识: google")
        else:
            print("2. 未找到转入交易")
            
    else:
        print(f"获取交易列表失败，状态码: {response_txs.status_code}")

except Exception as e:
    print(f"发生错误: {e}")
