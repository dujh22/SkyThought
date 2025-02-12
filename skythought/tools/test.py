import subprocess
import time
import os
import shutil

# 设置参数
dataset = "APPS"
model_path = "/workspace/dujh22/models/Qwen2.5-32B-Instruct"
tp = 8
max_tokens = 16384
split = "test"
source = "/workspace/dujh22/SkyThought/data/apps"
result_dir = "/workspace/dujh22/SkyThought/skythought/tools/test_data"
# num_iterations = 1000000  # 需要重复调用的次数


# 清空目录下的所有文件
def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 删除文件夹及其内容
            else:
                os.remove(file_path)  # 删除文件
        except Exception as e:
            print(f"删除文件 {file_path} 时发生错误: {e}")

# 循环调用
# for i in range(num_iterations):
i = 0
while True:
    i += 1
    print(f"开始第 {i+1} 次调用...")

    # 在每次调用之前清空目录
    clear_directory(result_dir)
    
    # 构建命令
    command = [
        "python", "inference_and_check.py",
        "--dataset", dataset,
        "--model", model_path,
        "--tp", str(tp),
        "--max_tokens", str(max_tokens),
        "--split", split,
        "--source", source,
        "--result-dir", result_dir
    ]
    
    try:
        # 执行命令
        subprocess.run(command, check=True)
        print(f"第 {i+1} 次调用成功")
    except subprocess.CalledProcessError as e:
        print(f"第 {i+1} 次调用失败: {e}")
    
    # 如果需要在每次调用之间暂停，可以设置暂停时间
    time.sleep(1)  # 暂停5秒