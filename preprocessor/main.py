import random


def remove_redundant_score(input_file, output_file):
    """
    由于有的同学在标注时直接在后面添加分数，而非修改，所以这个函数用来去除多余的分数
    :param input_file: 输入文件
    :param output_file: 输出文件
    :return: none
    """
    with open(input_file, 'r', newline='', encoding='utf-8') as file_in, \
            open(output_file, 'w', newline='', encoding='utf-8') as file_out:
        data = []
        for line in file_in:
            row = line.split("|")
            if len(row) > 3:
                row.pop(-2)
            data.append("|".join(row))

        for line in data:
            file_out.write(line)


def reduce_data(input_file, output_file):
    """
    数据集中中性情感的个数太多，该函数将每个数据集中中性情感控制在 40% 左右
    :param input_file: 输入文件
    :param output_file: 输出文件
    :return: none
    """
    data = []
    zeros_count = 0
    keep_zeros_count = 0

    # 读取文件并存储数据到列表
    with open(input_file, 'r', newline='', encoding='utf-8') as file_in:
        for line in file_in:
            data.append(line.strip())

    # 统计 0 的数量和需要保留的 0 的个数
    for line in data:
        row = line.split("|")
        if len(row) == 3:
            if row[-1].isdigit():
                if int(row[-1]) == 0:
                    zeros_count += 1

    keep_zeros_count = int(len(data) * 0.4)

    print("Zeros count:", zeros_count)
    print("keep_zeros_count", keep_zeros_count)

    # 随机删除多余的 0
    if zeros_count > keep_zeros_count:
        indexes = [i for i in range(len(data)) if data[i].split("|")[-1].isdigit() and int(data[i].split("|")[-1]) == 0]
        random.shuffle(indexes)
        delete_indexes = indexes[keep_zeros_count:]
        data = [row for i, row in enumerate(data) if i not in delete_indexes]

    # 写入处理后的数据到新的文件
    with open(output_file, 'w', newline='', encoding='utf-8') as file_out:
        for line in data:
            file_out.write(line + '\n')


if __name__ == '__main__':
    # 输入文件路径
    input_file_1 = 'comments.csv'
    input_file_2 = 'issues.csv'
    # 去除多余分数后文件路径
    processed_file_1 = 'comments_processed.csv'
    processed_file_2 = 'issues_processed.csv'
    # 输出文件路径
    output_file_1 = 'comments_processed_1.csv'
    output_file_2 = 'issues_processed_1.csv'

    remove_redundant_score(input_file_1, processed_file_1)
    remove_redundant_score(input_file_2, processed_file_2)

    reduce_data(processed_file_1, output_file_1)
    reduce_data(processed_file_2, output_file_2)
