# -*- coding: utf-8 -*-
# 把一维列表拆分成若干块
# 每块中含有N个元素

def split_to_blocks(org_list, N):
    '''
    org_list: 原始的元素列表
    N: number of elements in each block
    '''
    total = len(org_list)
    BLOCK_NUM = (total//N + 1) if (total % N) else total//N
    blocks = [[] for i in range(BLOCK_NUM)]
    for i in range(BLOCK_NUM):
        j = 0
        while j < N:
            index = i * N + j
            if index == total:
                break
            else:
                blocks[i].append(org_list[index])
                j += 1
    return blocks


# ============================= #
if __name__ == '__main__':
    total = 1000
    org_list = list(range(total))
    N = 19

    block = split_to_blocks(org_list, N)
