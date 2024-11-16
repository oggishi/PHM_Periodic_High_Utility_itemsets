import time

# Hàm đọc dữ liệu từ file
def read_data(file_path):
    transactions = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) < 3:
                continue  # Bỏ qua dòng không đúng định dạng

            items = list(map(int, parts[0].split()))
            transaction_utility = int(parts[1])  # Tổng utility của giao dịch (không dùng ở đây)
            item_utilities = list(map(int, parts[2].split()))

            # Tạo từ điển cho giao dịch
            transaction = {item: utility for item, utility in zip(items, item_utilities)}
            transactions.append(transaction)

    return transactions

# Hàm tính Real Utility cho mỗi mục
def calculate_real_utility(transactions):
    utilities = {}
    for transaction in transactions:
        for item, utility in transaction.items():
            if item in utilities:
                utilities[item] += utility
            else:
                utilities[item] = utility
    return utilities

# Hàm tính utility của itemset
def calculate_utility(itemset, transactions):
    total_utility = 0
    for transaction in transactions:
        total_utility += sum(transaction.get(item, 0) for item in itemset)
    return total_utility

# Hàm thêm itemset vào top-k queue
def add_to_top_k(itemset, utility, k):
    global top_k_queue
    if len(top_k_queue) < k:
        top_k_queue.append((itemset, utility))  # Thêm itemset vào danh sách
    else:
        # Nếu utility của itemset lớn hơn utility nhỏ nhất hiện tại, thay thế
        min_utility_itemset = min(top_k_queue, key=lambda x: x[1])  # Tìm itemset có utility nhỏ nhất
        if utility > min_utility_itemset[1]:
            top_k_queue.remove(min_utility_itemset)  # Loại bỏ itemset có utility nhỏ nhất
            top_k_queue.append((itemset, utility))  # Thêm itemset mới
    # Sắp xếp lại danh sách theo utility giảm dần
    top_k_queue = sorted(top_k_queue, key=lambda x: x[1], reverse=True)

# Hàm tìm kiếm trên các itemsets
def search_p(primary_items, transactions, negative_items, k):
    for item in primary_items:
        itemset = {item}
        utility = calculate_utility(itemset, transactions)
        if utility >= minUtil:
            add_to_top_k(itemset, utility, k)
            search_n(itemset, {i for i in primary_items if i != item}, transactions, negative_items, k)

def search_n(current_set, secondary_items, transactions, negative_items, k):
    for item in secondary_items.union(negative_items):  # Bao gồm cả negative items
        new_set = current_set | {item}
        utility = calculate_utility(new_set, transactions)
        if utility >= minUtil:
            add_to_top_k(new_set, utility, k)

# Đọc dữ liệu từ file và xử lý
filename = './data.txt'
transactions = read_data(filename)

# Cài đặt giá trị k và minUtil
k = 3
minUtil = 1

# Tính toán Real Utility cho mỗi item
real_utility = calculate_real_utility(transactions)

# Sắp xếp utility giảm dần và cập nhật minUtil
sorted_utilities = sorted(real_utility.values(), reverse=True)
minUtil = sorted_utilities[k-1] if len(sorted_utilities) >= k else minUtil

# Lọc các mục có utility >= minUtil và xác định negative items
filtered_items = {item for item, utility in real_utility.items() if utility >= minUtil}
negative_items = {item for item, utility in real_utility.items() if utility < 0}

# Lọc các giao dịch theo items đã được lọc
filtered_transactions = [{item: utility for item, utility in transaction.items() if item in filtered_items} for transaction in transactions]
filtered_transactions = [trans for trans in filtered_transactions if trans]

# Khởi tạo top-k queue
top_k_queue = []

# Chạy tìm kiếm trên các primary items
primary_items = filtered_items
start_time = time.time()

search_p(primary_items, filtered_transactions, negative_items, k)

# Thời gian thực thi
end_time = time.time()
execution_time = end_time - start_time

# In kết quả và thời gian thực thi
print("Top-k itemsets with utilities:")
for itemset, utility in top_k_queue:
    print(f"{itemset}: {utility}")
print(f"Execution Time: {execution_time} seconds")
