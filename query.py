import requests

address = "0x7Ce3c34b2c528330A2312B6621015D58B6FbCB61"

# 1. 获取账户基本信息
base_url = f"https://eth-sepolia.blockscout.com/api/v2/addresses/{address}"
# 2. 获取交易列表（不加任何额外参数，这样最不容易报错）
txs_url = f"{base_url}/transactions"

print("正在从区块链获取数据...")

try:
    # 第一步：查账户类型
    res_info = requests.get(base_url, timeout=30)
    if res_info.status_code == 200:
        is_contract = res_info.json().get('is_contract', False)
        print(f"1. 账户类型: {'contract' if is_contract else 'eoa'}")
    
    # 第二步：查交易列表
    res_txs = requests.get(txs_url, timeout=30)
    if res_txs.status_code == 200:
        items = res_txs.json().get('items', [])
        print(f"\n[成功获取到 {len(items)} 笔交易]\n")
        
        # 遍历打印每一笔交易的所有关键信息，供你拼 Flag 使用
        for i, tx in enumerate(items):
            # 获取交易哈希和区块高度
            tx_hash = tx.get('hash', 'N/A')
            block = tx.get('block', 'N/A')
            
            # 安全地获取 from 和 to (防止 None 崩溃)
            from_obj = tx.get('from')
            from_addr = from_obj.get('hash', '') if from_obj else ''
            
            to_obj = tx.get('to')
            to_addr = to_obj.get('hash', '') if to_obj else 'Contract Creation'
            
            # 获取 nonce 和 创建的合约地址
            nonce = tx.get('nonce', 'N/A')
            created = tx.get('created_contract')
            created_addr = created.get('hash', '') if created else 'N/A'
            
            print(f"--- 交易 {i+1} ---")
            print(f"区块: {block} | Nonce: {nonce}")
            print(f"From: {from_addr}")
            print(f"To:   {to_addr}")
            if created_addr != 'N/A':
                print(f"创建合约地址: {created_addr} (后8位: {created_addr[-8:]})")
            print("-" * 20)
            
    else:
        print(f"获取交易列表失败，状态码: {res_txs.status_code}")

except Exception as e:
    print(f"发生错误: {e}")
