import re
from collections import defaultdict

# 示例数据
data = [
    "XX一丁目",
    "XX二丁目",
    "YYY一丁目",
    "YY二丁目",
    "ZZ六丁目",
    "ZZ七丁目",
    "ZZZ二丁目"
]

# 使用 defaultdict 创建一个默认字典来存储分类结果
classified_data = defaultdict(list)

# 正则表达式模式，用于匹配开头的共同部分（非数字和非标点符号的连续字符）
pattern = re.compile(r"^[^\d一二三四五六七八九十丁目]+")
# 遍历数据并分类
for item in data:
    match = pattern.match(item)
    if match:
        key = match.group(0)  # 提取共同部分作为分类键
        classified_data[key].append(item)

# 打印分类结果
for key, values in classified_data.items():
    print(f"{key}: {values}")