import glob
import json
import math
import os
import random

folder_path = "./results/tests/"
json_files = glob.glob(os.path.join(folder_path, "*.json"))

data = []


def get_query_number(text):
    return "".join([char for char in text if char.isdigit()])


for json_file in json_files:
    name = json_file.split("/")[-1].replace(".json", "")
    with open(json_file, "r") as file:
        if os.path.getsize(json_file) != 0:
            json_data = json.load(file)
            json_data["query"] = f"{name}"
            json_data["query_number"] = int(get_query_number(name))
            data.append(json_data)


def get_parsed_data(base_folder_path):
    directories = [
        d
        for d in os.listdir(base_folder_path)
        if os.path.isdir(os.path.join(base_folder_path, d))
    ]
    lowest_for_query = {}
    data = []
    for i, dir in enumerate(sorted(directories)):
        json_files = glob.glob(os.path.join(f"{base_folder_path}{dir}", "*.json"))
        dir_data = {}
        for json_file in json_files:
            name = json_file.split("/")[-1].replace(".json", "")
            with open(json_file, "r") as file:
                if os.path.getsize(json_file) != 0:
                    json_data = json.load(file)
                    dir_data[name] = json_data["results"][0]["mean"]
                    if name in lowest_for_query:
                        if dir_data[name] < lowest_for_query[name]:
                            lowest_for_query[name] = dir_data[name]
                    else:
                        lowest_for_query[name] = dir_data[name]

        # print(dir_data)
        data.append({"dir": dir, "data": dir_data})

    # print("lowest_for_query")
    # print(lowest_for_query)

    return (data, lowest_for_query)


def calc_queries_in_relative_ranges():
    (data, lowest_for_query) = get_parsed_data(folder_path)

    results = []
    for dataset in data:
        ranges = [0] * 6
        # print(dataset)
        for k, v in dataset["data"].items():
            relative = v / lowest_for_query[k]
            # print(k, v, relative)
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

    print("""\\begin{table}[H]
\centering
\caption{Caption}
\\begin{tabularx}{\\textwidth}{l|l|l|l|l|l|l}
\\toprule
 & \\textbf{< 1.2} & \\textbf{[1.2, 1.5)} & \\textbf{[1.5, 2)} & \\textbf{[2, 5)} & \\textbf{[5, 10)} & \\textbf{> 10} \\\ \midrule""")
    for result in results:
        print(f"{result['dir']} & {' & '.join(result['ranges'])} \\\ ".replace('below_', 'b').replace('_above_', '\_a').replace('_level_', '\_l'))
    print("""\\bottomrule
\end{tabularx}
\end{table}""")

def most_speeded_up_query(dir: str):
    (data, lowest_for_query) = get_parsed_data(folder_path)
    baseline = list(filter(lambda x: x['dir'] == 'baseline', data))[0]['data']
    dir_data = list(filter(lambda x: x['dir'] == dir, data))[0]['data']
    # print(baseline)
    # print(dir_data)
    speeded_up = []

    for k, v in dir_data.items():
        diff = round(baseline[k] / v if v < baseline[k] else -(v / baseline[k]), 2)
        speeded_up.append([k, diff])

    sorted_speeded_up = sorted(speeded_up, key=lambda x: x[1])    
    print(sorted_speeded_up)

# calc_queries_in_relative_ranges()
    
most_speeded_up_query("below_32_above_32_level_45")
