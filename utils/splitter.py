import os
import pandas as pd


def split_csv_file(csv_file_path):
    # 读取原始 CSV 文件，指定分隔符为竖线 |
    df = pd.read_csv(csv_file_path, sep='|')
    total_rows = len(df)

    # 确定切分的小文件数量
    num_files = total_rows // 100
    if total_rows % 100 != 0:
        num_files += 1

    # 创建保存小文件的目录
    base_path = os.path.dirname(csv_file_path)
    output_dir = os.path.join(base_path, 'split_csv')
    os.makedirs(output_dir, exist_ok=True)

    # 切分并保存小文件
    for i in range(num_files):
        start_row = i * 100
        end_row = start_row + 100
        output_file_path = os.path.join(output_dir, f'split_file_{i + 1}.csv')
        df[start_row:end_row].to_csv(output_file_path, sep='|', index=False, header=False)

        print(f'Saved {output_file_path}')


# 示例用法
csv_file_path = 'stackoverflow_data.csv'
split_csv_file(csv_file_path)
