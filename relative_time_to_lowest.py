import glob
import json
import os
import numpy as np
import re

folder_path = "./results/tests/"
json_files = glob.glob(os.path.join(folder_path, "*.json"))

data = []


def get_query_number(text):
    return "".join([char for char in text if char.isdigit()])


def shorten_config_name(str: str) -> str:
    return str.replace("below_", "").replace("_above_", "\_").replace("_level_", "\_")

def sort_directories(dir: str) -> int:
    if dir == 'baseline': return -1
    numbers = re.findall(r'\d+', dir)
    numbers = [int(num) for num in numbers]
    return numbers[0] + (numbers[1] / 100) + (numbers[2] / 100)

def get_parsed_data(base_folder_path) -> tuple[list[dict], dict]:
    directories = [
        d
        for d in os.listdir(base_folder_path)
        if os.path.isdir(os.path.join(base_folder_path, d))
    ]
    lowest_for_query = {}
    data = []
    for i, dir in enumerate(sorted(directories, key=sort_directories)):
        json_files = glob.glob(os.path.join(f"{base_folder_path}{dir}", "*.json"))
        dir_data = {}
        dir_raw_data = {}
        for json_file in json_files:
            name = json_file.split("/")[-1].replace(".json", "")
            with open(json_file, "r") as file:
                if os.path.getsize(json_file) != 0:
                    json_data = json.load(file)
                    dir_data[name] = json_data["results"][0]["mean"]
                    dir_raw_data[name] = json_data["results"][0]
                    if name in lowest_for_query:
                        if dir_data[name] < lowest_for_query[name]:
                            lowest_for_query[name] = dir_data[name]
                    else:
                        lowest_for_query[name] = dir_data[name]

        data.append({"dir": dir, "data": dir_data, "raw_data": dir_raw_data})

    return (data, lowest_for_query)


def calc_queries_in_relative_ranges():
    (data, lowest_for_query) = get_parsed_data(folder_path)

    results = []
    for dataset in data:
        ranges = [0] * 6
        for k, v in dataset["data"].items():
            relative = v / lowest_for_query[k]
            if relative < 1.2:
                ranges[0] += 1
            elif relative < 1.5:
                ranges[1] += 1
            elif relative < 2:
                ranges[2] += 1
            elif relative < 5:
                ranges[3] += 1
            elif relative < 10:
                ranges[4] += 1
            else:
                ranges[5] += 1

        ranges = [f"{round((x / (len(dataset['data']))) * 100, 1)}\%" for x in ranges]

        results.append({"dir": dataset["dir"], "ranges": ranges})

    print(
        """\\begin{table}[H]
\centering
\caption{Caption}
\\begin{tabularx}{\\textwidth}{l|l|l|l|l|l|l}
\\toprule
 & \\textbf{< 1.2} & \\textbf{[1.2, 1.5)} & \\textbf{[1.5, 2)} & \\textbf{[2, 5)} & \\textbf{[5, 10)} & \\textbf{> 10} \\\ \midrule"""
    )
    for result in results:
        print(
            shorten_config_name(
                f"{result['dir']} & {' & '.join(result['ranges'])} \\\ "
            )
        )
    print(
        """\\bottomrule
\end{tabularx}
\end{table}"""
    )


def most_speeded_up_query(dir: str):
    (data, _) = get_parsed_data(folder_path)
    baseline = list(filter(lambda x: x["dir"] == "baseline", data))[0]["data"]
    dir_data = list(filter(lambda x: x["dir"] == dir, data))[0]["data"]
    speeded_up = []

    for k, v in dir_data.items():
        diff = round(baseline[k] / v if v < baseline[k] else -(v / baseline[k]), 2)
        speeded_up.append([k, diff])

    sorted_speeded_up = sorted(speeded_up, key=lambda x: x[1])
    print(sorted_speeded_up)


def std_deviations(data, max_in_config = False):
    (data, _) = get_parsed_data(folder_path)

    yticklabels = []

    for index, configuration in enumerate(data):
        yticklabels.append(shorten_config_name(configuration["dir"]))
        if max_in_config:
            q = max(configuration["raw_data"].values(), key=lambda x: x["stddev"])
            data_array = np.array(q["times"])
        else:
            data_array = np.array(list(
                map(lambda x: x["stddev"], configuration["raw_data"].values())
            ))

        # Calculate minimum and maximum
        minimum = np.min(data_array)
        maximum = np.max(data_array)
        # Calculate quartiles
        q1 = np.percentile(data_array, 25)
        q3 = np.percentile(data_array, 75)
        # Calculate median
        median = np.median(data_array)

        print(
            f"""\\addplot [
  boxplot prepared={{median={median}, upper quartile={q3}, lower quartile={q1}, lower whisker={minimum}, upper whisker={maximum}, draw position={index}}},
] coordinates {{}};"""
        )

    print(','.join(yticklabels))


calc_queries_in_relative_ranges()

# most_speeded_up_query("below_128_above_32_level_50")

# std_deviations(data, True)
