import subprocess
import os
from datetime import datetime, timedelta

# 路径到你的_notes目录
# 获取当前执行脚本的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构造_notes目录的相对路径
notes_dir = os.path.join(script_dir, '../_notes')
notify_file = os.path.join(script_dir, 'review_notify.txt')

# 指定时间间隔的天数
# 此天数根据艾宾浩斯遗忘曲线配置，分别为3天、5天、10天、1月、3月、1年
days_intervals = [3,5,10,30,90,365]

def get_last_modified_times(file_path):
    # 使用git blame获取每一行的最后修改时间
    cmd = ['git', '-C', notes_dir, 'blame', '--date=iso', '--',file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return ""

def process_files():
    with open(notify_file, 'w') as f_notify:
        for root, dirs, files in os.walk(notes_dir):
            for file_name in files:
                if file_name.endswith('.md'):
                    file_path = os.path.join(root, file_name)
                    relative_file_path = os.path.relpath(file_path, notes_dir)
                    file_content = get_last_modified_times(relative_file_path)
                    for line in file_content.split('\n'):
                        if " " in line:  # 确保是有效的行
                            parts = line.split(')')
                            if len(parts) > 1:
                                line_info = parts[0]
                                line_content = parts[1].strip()
                                line_number = line_info.split()[-1]
                                date_str = ' '.join(line_info.split()[-4:-2])
                                try:
                                    last_modified_date = datetime.fromisoformat(date_str)
                                    age = (datetime.now() - last_modified_date).days
                                    if age in days_intervals:
                                        f_notify.write(f"/_notes/{relative_file_path}:{line_number} {age} days ago - {line}\n")
                                except ValueError:
                                    continue

if __name__ == "__main__":
    process_files()