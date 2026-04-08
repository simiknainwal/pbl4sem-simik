def _default_key(x):
    return x


def merge(arr, low, mid, high, key):
    temp = []
    
    i = low
    j = mid + 1
    
    while i <= mid and j <= high:
        if key(arr[i]) <= key(arr[j]):
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1
    
    while i <= mid:
        temp.append(arr[i])
        i += 1
        
    while j <= high:
        temp.append(arr[j])
        j += 1
    
    for k in range(len(temp)):
        arr[low + k] = temp[k]


def sort(arr, low, high, key):
    if low == high:
        return
    
    mid = low + (high - low) // 2
    
    sort(arr, low, mid, key)
    sort(arr, mid + 1, high, key)
    merge(arr, low, mid, high, key)


def merge_sort(arr, key=None):
    if key is None:
        key = _default_key
    
    if len(arr) > 0:
        sort(arr, 0, len(arr) - 1, key)
    
    return arr