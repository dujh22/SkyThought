import argparse
import subprocess
import os
import json

# Define eval to split mapping
eval_to_split = {
  "MATH500": "test", 
  "AIME": "train", 
  "GPQADiamond": "train", 
  "MMLU": "test",
  "LiveCodeBench": "test"
}

def parse_arguments():
    # 创建一个ArgumentParser对象，用于处理命令行参数
    parser = argparse.ArgumentParser(description="Process model path, prompt format, and evals to run.")
    # 添加一个命令行参数，用于指定模型的路径
    parser.add_argument("--model", required=True, type=str, help="Path to the model.")
    # 添加一个命令行参数，用于指定要运行的evals
    parser.add_argument("--evals", required=True, type=str, help="Comma-separated list of evals to run (no spaces).")
    # 添加一个命令行参数，用于指定Tensor Parallelism Degree, tp（Tensor Parallelism Degree）通常用于指定张量并行度的程度。在深度学习中，尤其是在使用大型模型时，张量并行可以帮助将模型的计算分散到多个 GPU 上，从而提高训练效率和速度。设置 tp 的值为 8 意味着模型的计算将被分配到 8 个 GPU 上进行并行处理。
    parser.add_argument("--tp", type=int, default=8, help="Tensor Parallelism Degree")
    # 添加一个命令行参数，用于指定是否过滤难度
    parser.add_argument("--filter-difficulty", action="store_true", help="Filter difficulty.")
    # 添加一个命令行参数，用于指定数据集的来源
    parser.add_argument("--source", type=str, help="Source for the dataset.")
    # 添加一个命令行参数，用于指定输出结果的文件
    parser.add_argument("--output_file", required=True, type=str, help="Output file to write results to.")
    # 返回解析后的命令行参数
    return parser.parse_args()

def extract_accuracy_from_output(output):
    # Iterate through all lines from the end to the beginning
    lines = output.splitlines()[::-1]
    for line in lines:
        try:
            # Attempt to parse a JSON object from the line
            data = json.loads(line.replace("'", '"'))
            if "acc" in data:
                return data["acc"]
        except json.JSONDecodeError:
            continue 
    return None

def write_logs_to_file(logs, output_file):
    try:
        with open(output_file, "w") as file:
            file.write(logs)
        print(f"Logs successfully written to {output_file}")
    except IOError as e:
        print(f"Failed to write logs to file {output_file}: {e}")

def main():
    args = parse_arguments()

    # Extract the arguments
    model_path = args.model
    evals = args.evals.split(",")
    output_file = args.output_file
    tp = args.tp

    script_path = "inference_and_check.py"

    # Hold all logs 
    all_logs = ""
    results = {}

    # Run the Python command for each eval and collect logs
    for eval_name in evals:
        command = [
            "python", script_path, 
            "--model", model_path, 
            "--dataset", eval_name, 
            "--split", eval_to_split[eval_name], 
            "--tp", str(tp)]
        if args.filter_difficulty:
            assert args.source != "", "No source passed for filtering difficulty."
            command.append("--filter-difficulty")
            command.append("--source")
            command.append(args.source)
        print(f"Running eval {eval_name} with command {command}")
        all_logs += f"\nRunning eval: {eval_name} with command {command}\n"
        try:
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as proc:
                output_lines = []
                for line in proc.stdout:
                    print(line, end="")  # Stream output to the console
                    output_lines.append(line)
                    all_logs += line
                proc.wait()
                if proc.returncode != 0:
                    raise subprocess.CalledProcessError(proc.returncode, command)

                # Capture output for post-processing
                output = "".join(output_lines)
                accuracy = extract_accuracy_from_output(output)
                results[eval_name] = accuracy

        except subprocess.CalledProcessError as e:
            error_message = f"Error occurred while running eval {eval_name}: {e}\n"
            print(error_message)
            all_logs += error_message

    # Write logs of all stdout / stderr to a file
    write_logs_to_file(all_logs, output_file)

    print("Results:")
    print(results)

if __name__ == "__main__":
    main()
