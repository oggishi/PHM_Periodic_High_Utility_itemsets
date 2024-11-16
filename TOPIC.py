import time

# Hàm đọc dữ liệu từ file
def read_data(file_path):
    transactions = []
    start_reading_time = time.time()  # Thời gian bắt đầu đọc dữ liệu
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) < 3:
                continue  # Bỏ qua các dòng không đúng định dạng

            # Danh sách các item trong giao dịch
            items = list(map(int, parts[0].split()))
            item_utilities = list(map(int, parts[2].split()))

            # Tạo từ điển cho giao dịch
            transaction = {item: utility for item, utility in zip(items, item_utilities)}
            transactions.append(transaction)

    end_reading_time = time.time()  # Thời gian kết thúc đọc dữ liệu
    reading_duration = end_reading_time - start_reading_time
    print(f"Data reading time: {reading_duration:.4f} seconds")
    
    return transactions

# Tính toán mức độ hữu ích thực sự (Real Utility) cho từng item
def calculate_real_utility(transactions):
    utilities = {}
    for transaction in transactions:
        for item, utility in transaction.items():
            if item in utilities:
                utilities[item] += utility
            else:
                utilities[item] = utility
    return utilities

# Tính toán Raised Support Utility (RSU) của itemset
def calculate_RSU(itemset, transactions):
    total_utility = 0
    for transaction in transactions:
        # Tính RSU cho itemset bằng cách cộng tất cả các mức độ hữu ích của các item trong itemset
        transaction_utility = sum(transaction.get(item, 0) for item in itemset)
        total_utility += transaction_utility
    return total_utility

# Tính toán Real Level Utility (RLU) của itemset
def calculate_RLU(itemset, transactions):
    total_utility = 0
    for transaction in transactions:
        # Tính RLU cho itemset bằng cách cộng tất cả các mức độ hữu ích của các item trong itemset
        transaction_utility = sum(transaction.get(item, 0) for item in itemset)
        total_utility += transaction_utility
    return total_utility

# Cập nhật minUtil theo thuật toán trong bài báo
def update_minUtil(RIU, k):
    sorted_utility = sorted(RIU, reverse=True)  # Sắp xếp giảm dần
    if len(sorted_utility) >= k:
        return sorted_utility[k-1]  # Lấy giá trị thứ k
    return 1  # Nếu không đủ, đặt minUtil là 1

# Hàm thêm itemset vào top-k list và thực hiện pruning
def add_to_top_k(itemset, utility):
    global top_k_queue, minUtil  # Đảm bảo khai báo minUtil là global
    # Nếu itemset đã có trong top_k_queue, không thêm vào
    if any(existing_itemset == itemset for existing_itemset, _ in top_k_queue):
        return

    # Nếu chưa có đủ k phần tử, thêm itemset vào danh sách
    if len(top_k_queue) < k:
        top_k_queue.append((itemset, utility))
        top_k_queue = sorted(top_k_queue, key=lambda x: x[1], reverse=True)
    # Nếu utility của itemset lớn hơn utility của itemset nhỏ nhất trong top-k, cập nhật top-k
    elif utility > top_k_queue[-1][1]:
        top_k_queue[-1] = (itemset, utility)
        top_k_queue = sorted(top_k_queue, key=lambda x: x[1], reverse=True)
        minUtil = top_k_queue[-1][1]

# Thuật toán cắt tỉa và tìm kiếm với các itemsets có hữu ích cao (Primary items)
def search_p(primary_items, transactions, negative_items):
    global minUtil  # Đảm bảo khai báo minUtil là global
    for item in primary_items:
        itemset = {item}
        utility = calculate_RSU(itemset, transactions)  # Sử dụng calculate_RSU thay vì calculate_utility
        if utility >= minUtil:
            add_to_top_k(itemset, utility)
            search_n(itemset, {i for i in primary_items if i != item}, transactions, negative_items)

# Hàm tìm kiếm với các itemsets phụ (secondary items) và thực hiện pruning
def search_n(current_set, secondary_items, transactions, negative_items):
    global minUtil  # Đảm bảo khai báo minUtil là global
    for item in secondary_items.union(negative_items):  # Bao gồm cả item với utility âm
        new_set = current_set | {item}
        utility = calculate_RSU(new_set, transactions)  # Sử dụng calculate_RSU thay vì calculate_utility
        if utility >= minUtil:  # Chỉ thêm vào nếu mức độ hữu ích >= minUtil
            add_to_top_k(new_set, utility)

# Cắt tỉa giao dịch (scan D) - Chỉ giữ lại các giao dịch có itemsets có hữu ích
def prune_transactions(transactions, filtered_items):
    pruned_transactions = []
    for transaction in transactions:
        pruned_transaction = {item: utility for item, utility in transaction.items() if item in filtered_items}
        if pruned_transaction:
            pruned_transactions.append(pruned_transaction)
    return pruned_transactions

# Thuật toán chính - Tìm kiếm Top-k itemsets với mức độ hữu ích cao nhất
def run_top_k_mining(filename, k, min_util_threshold):
    global minUtil  # Đảm bảo khai báo minUtil là global
    start_total_time = time.time()  # Thời gian bắt đầu toàn bộ quá trình

    # Đọc dữ liệu từ file
    transactions = read_data(filename)
    
    # Tính toán mức độ hữu ích thực sự cho từng item
    real_utility = calculate_real_utility(transactions)

    # Sắp xếp các mức độ hữu ích theo thứ tự giảm dần và cập nhật minUtil
    sorted_utilities = sorted(real_utility.values(), reverse=True)
    minUtil = sorted_utilities[k-1] if len(sorted_utilities) >= k else min_util_threshold

    # Lọc các mặt hàng có mức độ hữu ích >= minUtil
    filtered_items = {item for item, utility in real_utility.items() if utility >= minUtil}

    # Thu thập các item với mức độ hữu ích âm
    negative_items = {item for item, utility in real_utility.items() if utility < 0}

    # Cắt tỉa giao dịch - Lọc các giao dịch chỉ giữ các item có mức độ hữu ích >= minUtil
    filtered_transactions = prune_transactions(transactions, filtered_items)

    # Cập nhật minUtil theo giải thuật trong bài báo
    minUtil = update_minUtil(list(real_utility.values()), k)

    # Khởi tạo danh sách top-k
    global top_k_queue
    top_k_queue = []

    # Tiến hành tìm kiếm với các item chính (Primary items)
    start_search_time = time.time()  # Thời gian bắt đầu tìm kiếm
    search_p(filtered_items, filtered_transactions, negative_items)
    end_search_time = time.time()  # Thời gian kết thúc tìm kiếm

    search_duration = end_search_time - start_search_time
    print(f"Search time: {search_duration:.4f} seconds")

    # Tổng thời gian chạy
    end_total_time = time.time()  # Thời gian kết thúc toàn bộ quá trình
    total_duration = end_total_time - start_total_time
    print(f"Total runtime: {total_duration:.4f} seconds")

    # Hiển thị kết quả
    # print("Top-k itemsets with utilities:")
    # for itemset, utility in top_k_queue:  
    #     print(f"{itemset}: {utility}")

# Thực thi
filename = './mushroom.txt'
k = 1000  # Số lượng itemsets top-k bạn muốn
min_util_threshold = 1  # Ngưỡng hữu ích tối thiểu
run_top_k_mining(filename, k, min_util_threshold)
