import time
import heapq  # Để sử dụng priority queue

# Hàm đọc dữ liệu từ file txt và chuyển đổi thành dạng list của các giao dịch
def read_data(file_path):
    transactions = []
    with open(file_path, "r") as file:
        for line in file:
            # Phân tách các phần tử trong dòng
            parts = line.strip().split(":")
            if len(parts) < 3:
                continue  # Bỏ qua dòng không đúng định dạng

            # Danh sách các mục trong giao dịch
            items = list(map(int, parts[0].split()))
            transaction_utility = int(parts[1])  # Tổng utility của giao dịch (có thể không dùng)
            item_utilities = list(map(int, parts[2].split()))

            # Tạo một từ điển cho giao dịch này
            transaction = {item: utility for item, utility in zip(items, item_utilities)}
            transactions.append(transaction)

    return transactions

# Tính tổng giá trị hữu ích (Utility) của tập hợp mục
def calculate_utility(itemset, dataset):
    utility = 0
    for transaction in dataset:
        # Tính utility cho từng mục trong itemset nếu nó có trong transaction
        utility += sum(transaction.get(item, 0) for item in itemset)
    return utility

# Tạo các tập hợp con từ danh sách các mục
def generate_combinations(items):
    itemsets = []
    n = len(items)
    # Tạo tất cả các tập hợp con (không bao gồm tập hợp rỗng)
    for i in range(1, 1 << n):  # 1 << n là 2^n
        itemset = []
        for j in range(n):
            if i & (1 << j):  # Kiểm tra bit j trong số i
                itemset.append(items[j])
        itemsets.append(tuple(itemset))  # Chuyển thành tuple để tránh list mutable
    return itemsets

# Tính Real Utility (RIU) của tất cả các item
def calculate_real_utility(dataset):
    utilities = {}
    for transaction in dataset:
        for item, utility in transaction.items():
            if item in utilities:
                utilities[item] += utility
            else:
                utilities[item] = utility
    return utilities

# Thuật toán TopHUI - tìm các itemset có hữu ích cao nhất
def top_HUI(dataset, k=3):
    # Lấy tất cả các mục duy nhất từ dataset
    all_items = set()
    for transaction in dataset:
        all_items.update(transaction.keys())
    
    # Tính Real Utility (RIU) cho tất cả các mục
    real_utilities = calculate_real_utility(dataset)
    
    # Sắp xếp theo Utility giảm dần để lấy minUtility
    sorted_utilities = sorted(real_utilities.values(), reverse=True)
    minUtil = sorted_utilities[k-1] if len(sorted_utilities) >= k else minUtil

    # Tạo tất cả các tập hợp con của các mục (tất cả các kết hợp các mục từ 1 đến len(all_items))
    itemsets = generate_combinations(sorted(all_items))
    
    # Tính utility cho từng itemset và lưu kết quả
    itemset_utilities = []
    for itemset in itemsets:
        utility = calculate_utility(itemset, dataset)
        itemset_utilities.append((itemset, utility))
    
    # Sắp xếp theo utility giảm dần và chọn k tập hợp mục có ích cao nhất
    itemset_utilities.sort(key=lambda x: x[1], reverse=True)
    
    # Priority queue cho top k itemsets
    top_k_queue = []
    
    # Đảm bảo chỉ giữ top-k itemsets với utility cao nhất
    for itemset, utility in itemset_utilities:
        if len(top_k_queue) < k:
            heapq.heappush(top_k_queue, (utility, itemset))
        else:
            if utility > top_k_queue[0][0]:  # Nếu utility của itemset hiện tại cao hơn minUtil
                heapq.heapreplace(top_k_queue, (utility, itemset))
    
    # Trả về top-k itemsets
    top_k_itemsets = [(itemset, utility) for utility, itemset in top_k_queue]
    
    return top_k_itemsets

# Đo thời gian chạy
start_time = time.time()

# Đọc dữ liệu từ file
filename = './mushroom.txt'  # Tên file dữ liệu
dataset = read_data(filename)

# Chạy thuật toán TopHUI với dataset và k = 100
top_k_itemsets = top_HUI(dataset, k=10)

# In kết quả
print("\nTop-K High Utility Itemsets:")
for itemset, utility in top_k_itemsets:
    itemset_str = ' '.join(map(str, itemset))  # Chuyển itemset thành chuỗi không có dấu phẩy
    print(f"Itemset: {itemset_str}, Utility: {utility}")

# In thời gian chạy
end_time = time.time()
print(f"\nThời gian chạy: {end_time - start_time:.6f} giây")
