import glob
import json
import math
import os
import random
import re
import shutil

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

data = []


def get_query_number(text):
    return "".join([char for char in text if char.isdigit()])


# folders = ["./results/tests/base_tests/"]
#
# for folder in folders:
#     json_files = glob.glob(os.path.join(folder, "*.json"))
#     for json_file in json_files:
#         name = json_file.split("/")[-1].replace(".json", "")
#         with open(json_file, "r") as file:
#             if os.path.getsize(json_file) != 0:
#                 json_data = json.load(file)
#                 json_data["query"] = f"{name}"
#                 json_data["query_number"] = int(get_query_number(name))
#                 data.append(json_data)
#
#
# dfs = [
#     pd.json_normalize(query["results"], sep="_").assign(
#         query=query["query"], query_number=query["query_number"]
#     )
#     for query in data
# ]
#
# df = pd.concat(dfs, ignore_index=True)


def get_all_command_variants(base_folder_path, command_func=None):
    directories = [
        d
        for d in os.listdir(base_folder_path)
        if os.path.isdir(os.path.join(base_folder_path, d))
    ]
    data = []
    for dir in directories:
        json_files = glob.glob(os.path.join(f"{base_folder_path}{dir}", "*.json"))
        for json_file in json_files:
            name = json_file.split("/")[-1].replace(".json", "")
            with open(json_file, "r") as file:
                if os.path.getsize(json_file) != 0:
                    json_data = json.load(file)
                    json_data["query"] = f"{name}"
                    json_data["query_number"] = int(get_query_number(name))
                    command = f"{dir}"
                    if command_func is not None and command != "baseline":
                        json_data["results"][0]["command"] = command_func(f"{dir}")
                    else:
                        json_data["results"][0]["command"] = command

                    data.append(json_data)
    dfs = [
        pd.json_normalize(query["results"], sep="_").assign(
            query=query["query"], query_number=query["query_number"]
        )
        for query in data
    ]

    return pd.concat(dfs, ignore_index=True)


def create_compare_df(data, compare_command):
    filter_data = data[(data["command"].isin(["baseline", compare_command]))]
    filter_data.loc[data["command"] == "baseline", "command"] = "without_reoptimization"
    filter_data.loc[data["command"] == compare_command, "command"] = (
        "with_reoptimization"
    )
    return filter_data


def custom_sort(query):
    numeric_part, alphabetic_part = "", ""
    for char in query:
        if char.isdigit():
            numeric_part += char
        else:
            alphabetic_part += char

    return int(numeric_part), alphabetic_part


def split_df(data_df):
    splits = math.ceil(len(data_df) / 20)

    total_rows = len(data_df)
    rows_per_part = math.ceil(total_rows / splits)

    split_dfs = [
        data_df.iloc[i * rows_per_part : (i + 1) * rows_per_part] for i in range(splits)
    ]

    num_rows = math.ceil(splits / 3)
    num_cols = min(splits, 3)
    return split_dfs, num_rows, num_cols


# df = df.sort_values(by=["query"], key=lambda x: x.apply(custom_sort))


sns.set_theme()

colors = {"with_reoptimization": "blue", "without_reoptimization": "lightgreen"}

hue_order = ["with_reoptimization", "without_reoptimization"]


def plot_all(df, save=False):
    split_dfs, num_rows, num_cols = split_df(df)

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(15, 5 * num_rows))
    axes = axes.flatten()
    for part_df, ax in zip(split_dfs, axes):
        bar = sns.barplot(
            data=part_df,
            x="query",
            y="median",
            hue="command",
            edgecolor="black",
            palette=colors,
            legend=False,
            ci=None,
            dodge=True,
            alpha=0.7,
            ax=ax,
        )
        bar.set_ylim(0, max(part_df["median"]))
        bar.set_ylabel("Median seconds")

    legend_labels = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label="with_reoptimization",
            markerfacecolor=colors["with_reoptimization"],
            markersize=10,
        ),
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label="without_reoptimization",
            markerfacecolor=colors["without_reoptimization"],
            markersize=10,
        ),
    ]

    fig.legend(handles=legend_labels, title="Command", loc="upper left")

    plt.tight_layout()
    if save:
        plt.savefig("./images/all-data.png")
    plt.show()


def plot_query(df, query_num, save=False):
    query_df = df[df["query_number"] == query_num]
    bar = sns.barplot(
        data=query_df,
        x="query",
        y="median",
        hue="command",
        edgecolor="black",
        palette=colors,
        ci=None,
        dodge=True,
        alpha=0.7,
    )
    bar.set_ylabel("Median seconds")
    if save:
        plt.savefig(f"./images/data-{query_num}.png")
    plt.show()


def plot_query_range(df, lower, upper, save=False):
    query_df = df[(df["query_number"] >= lower) & (df["query_number"] <= upper)]
    bar = sns.barplot(
        data=query_df,
        x="query",
        y="median",
        hue="command",
        edgecolor="black",
        palette=colors,
        ci=None,
        dodge=True,
        alpha=0.7,
    )

    bar.set_ylabel("Median seconds")

    if save:
        plt.savefig(f"./images/data-query-{lower}-to-{upper}.png")
    plt.show()


def plot_all_no_split(df, save=False):
    bar = sns.barplot(
        data=df,
        x="query",
        y="median",
        hue="command",
        edgecolor="black",
        palette=colors,
        ci=None,
        dodge=True,
        alpha=0.7,
    )

    bar.set_ylabel("Median seconds")

    if save:
        plt.savefig(f"./images/data-query-not-split.png")
    plt.show()


def plot_group_by_without_time(df, save=False):
    df_without = df[df["command"] == "without_reoptimization"]
    df_with = df[df["command"] == "with_reoptimization"]

    df_with = df_with.sort_values(by=["query"], key=lambda x: x.apply(custom_sort))
    df_without = df_without.sort_values(
        by=["query"], key=lambda x: x.apply(custom_sort)
    )

    new_df = pd.merge(df_with, df_without, on="query", suffixes=("_with", "_without"))

    sorted_df = new_df.sort_values(by="median_without")

    sns.barplot(
        data=sorted_df,
        x="query",
        y="median_with",
        edgecolor="black",
        color=colors["with_reoptimization"],
        legend=False,
        ci=None,
        alpha=0.5,
        dodge=True,
    )
    sns.barplot(
        data=sorted_df,
        x="query",
        y="median_without",
        edgecolor="black",
        color=colors["without_reoptimization"],
        legend=False,
        ci=None,
        alpha=0.5,
        dodge=True,
    )

    legend_labels = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label="with_reoptimization",
            markerfacecolor=colors["with_reoptimization"],
            markersize=10,
        ),
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label="without_reoptimization",
            markerfacecolor=colors["without_reoptimization"],
            markersize=10,
        ),
    ]

    plt.ylabel("Median seconds")
    plt.legend(handles=legend_labels, title="Command", loc="upper left")

    plt.tight_layout()
    if save:
        plt.savefig("./images/all-data-sorted.png")
    plt.show()


def side_plot_all(df, save=False, name=None):
    df_without = df[df["command"] == "without_reoptimization"]
    df_with = df[df["command"] == "with_reoptimization"]

    df_with = df_with.sort_values(by=["query"], key=lambda x: x.apply(custom_sort))
    df_without = df_without.sort_values(
        by=["query"], key=lambda x: x.apply(custom_sort)
    )
    new_df = pd.merge(df_with, df_without, on="query", suffixes=("_with", "_without"))

    sorted_df = new_df.sort_values(by="median_without")
    split_dfs, num_rows, num_cols = split_df(sorted_df)

    fig, axes = plt.subplots(
        nrows=num_rows, ncols=num_cols, figsize=(40, 20 * num_rows)
    )
    fontsize = 50
    axes = axes.flatten()
    bar_width = 0.35
    for part_df, ax in zip(split_dfs, axes):
        part_df.sort_values(by="median_without", ascending=False, inplace=True)
        part_df.reset_index(drop=True, inplace=True)
        y = range(len(part_df))

        ax.barh(
            y,
            part_df["median_with"],
            color="r",
            height=bar_width,
            label="With",
            edgecolor="black",
            alpha=0.5,
        )
        ax.barh(
            [i + bar_width for i in y],
            part_df["median_without"],
            color="b",
            height=bar_width,
            label="Without",
            hatch="/",
            edgecolor="black",
            alpha=0.5,
        )

        ax.set_yticks([i + bar_width / 2 for i in y])
        ax.set_yticklabels(part_df["query"])

        ax.set_xlabel("Median seconds", fontsize=fontsize)
        ax.tick_params(axis="both", which="major", labelsize=fontsize)
        # Add a legend and informative axis label
        sns.despine(left=True, bottom=True)
        handles, labels = axes[0].get_legend_handles_labels()
        unique_labels = list(set(labels))
        combined_handles = [handles[labels.index(label)] for label in unique_labels]
        fig.legend(
            combined_handles,
            unique_labels,
            ncol=2,
            loc="lower center",
            frameon=True,
            fontsize=fontsize,
        )

    if save:
        imageName = (
            f"./images/{name}/all-quries.eps" if name else f"./images/all-quries.eps"
        )
        plt.savefig(imageName, format="eps", bbox_inches="tight")

        return
    plt.tight_layout()
    plt.show()


def side_plot_all_no_split(df, save=False):
    df_without = df[df["command"] == "without_reoptimization"]
    df_with = df[df["command"] == "with_reoptimization"]

    df_with = df_with.sort_values(by=["query"], key=lambda x: x.apply(custom_sort))
    df_without = df_without.sort_values(
        by=["query"], key=lambda x: x.apply(custom_sort)
    )
    new_df = pd.merge(df_with, df_without, on="query", suffixes=("_with", "_without"))

    sorted_df = new_df.sort_values(by="median_without")

    sns.set_color_codes("pastel")
    sns.barplot(
        x="median_without",
        y="query",
        data=sorted_df,
        color="b",
        legend=False,
        label="Without",
        edgecolor="black",
        linestyle="dotted",
    )

    sns.set_color_codes("muted")

    bar = sns.barplot(
        x="median_with",
        y="query",
        data=sorted_df,
        color="b",
        legend=False,
        label="With",
        alpha=0.7,
        edgecolor="black",
    )
    bar.set_xlabel("Median seconds")

    # Add a legend and informative axis label
    sns.despine(left=True, bottom=True)

    if save:
        plt.savefig("./images/all-data-sorted.png")
    plt.show()


def side_plot_quey(df, query_num, save=False):
    query_df = df[df["query_number"] == query_num]
    df_without = query_df[query_df["command"] == "without_reoptimization"]
    df_with = query_df[query_df["command"] == "with_reoptimization"]
    new_df = pd.merge(df_with, df_without, on="query", suffixes=("_with", "_without"))
    fig, ax = plt.subplots(figsize=(6, 15))

    sns.set_color_codes("pastel")
    sns.barplot(
        x="median_without",
        y="query",
        data=new_df,
        color="b",
        legend=False,
        label="Without",
        edgecolor="black",
        linestyle="dotted",
    )

    # Plot the crashes where alcohol was involved
    sns.set_color_codes("muted")

    bar = sns.barplot(
        x="median_with",
        y="query",
        data=new_df,
        color="b",
        legend=False,
        label="With",
        alpha=0.7,
        edgecolor="black",
    )
    bar.set_xlabel("Median seconds")

    # Add a legend and informative axis label
    sns.despine(left=True, bottom=True)
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = list(set(labels))
    combined_handles = [handles[labels.index(label)] for label in unique_labels]
    fig.legend(combined_handles, unique_labels, ncol=2, loc="lower right", frameon=True)

    if save:
        plt.savefig(f"./images/side-plot-query-{query_num}.png")
    plt.show()


def side_plot_queries(data, query_nums, save=False):
    query_df = data[data["query_number"].isin(query_nums)]
    df_without = query_df[query_df["command"] == "without_reoptimization"]
    df_with = query_df[query_df["command"] == "with_reoptimization"]
    new_df = pd.merge(df_with, df_without, on="query", suffixes=("_with", "_without"))
    fig, ax = plt.subplots(figsize=(6, 15))

    sns.set_color_codes("pastel")
    sns.barplot(
        x="median_without",
        y="query",
        data=new_df,
        color="b",
        legend=False,
        label="Without",
        edgecolor="black",
        linestyle="dotted",
    )

    # Plot the crashes where alcohol was involved
    sns.set_color_codes("muted")

    bar = sns.barplot(
        x="median_with",
        y="query",
        data=new_df,
        color="b",
        legend=False,
        label="With",
        alpha=0.7,
        edgecolor="black",
    )
    bar.set_xlabel("Median seconds")

    # Add a legend and informative axis label
    sns.despine(left=True, bottom=True)
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = list(set(labels))
    combined_handles = [handles[labels.index(label)] for label in unique_labels]
    fig.legend(combined_handles, unique_labels, ncol=2, loc="lower right", frameon=True)

    if save:
        plt.savefig(f"./images/side-plot-queries-{'-'.join(query_nums)}.png")
    plt.show()


def side_plot_top_n_slowest(df, n, save=False):
    df_without = df[df["command"] == "without_reoptimization"]
    df_with = df[df["command"] == "with_reoptimization"]
    new_df = pd.merge(df_with, df_without, on="query", suffixes=("_with", "_without"))

    top_df = new_df.nlargest(n, "median_without")
    fig, ax = plt.subplots(figsize=(6, 15))

    sns.set_color_codes("pastel")
    sns.barplot(
        x="median_without",
        y="query",
        data=top_df,
        color="b",
        legend=False,
        label="Without",
        edgecolor="black",
        linestyle="dotted",
    )

    # Plot the crashes where alcohol was involved
    sns.set_color_codes("muted")

    bar = sns.barplot(
        x="median_with",
        y="query",
        data=top_df,
        color="b",
        legend=False,
        label="With",
        alpha=0.7,
        edgecolor="black",
    )
    bar.set_xlabel("Median seconds")

    # Add a legend and informative axis label
    sns.despine(left=True, bottom=True)
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = list(set(labels))
    combined_handles = [handles[labels.index(label)] for label in unique_labels]
    fig.legend(combined_handles, unique_labels, ncol=2, loc="lower right", frameon=True)

    if save:
        plt.savefig(f"./images/top-{n}-slowest.png")
    plt.show()


def side_plot_top_n_fastest(df, n, save=False):
    df_without = df[df["command"] == "without_reoptimization"]
    df_with = df[df["command"] == "with_reoptimization"]
    new_df = pd.merge(df_with, df_without, on="query", suffixes=("_with", "_without"))

    top_df = new_df.nsmallest(n, "median_without")
    fig, ax = plt.subplots(figsize=(6, 15))

    sns.set_color_codes("pastel")
    sns.barplot(
        x="median_without",
        y="query",
        data=top_df,
        color="b",
        legend=False,
        label="Without",
        edgecolor="black",
        linestyle="dotted",
    )

    # Plot the crashes where alcohol was involved
    sns.set_color_codes("muted")

    bar = sns.barplot(
        x="median_with",
        y="query",
        data=top_df,
        color="b",
        legend=False,
        label="With",
        alpha=0.7,
        edgecolor="black",
    )
    bar.set_xlabel("Median seconds")

    # Add a legend and informative axis label
    sns.despine(left=True, bottom=True)
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = list(set(labels))
    combined_handles = [handles[labels.index(label)] for label in unique_labels]
    fig.legend(combined_handles, unique_labels, ncol=2, loc="lower right", frameon=True)

    if save:
        plt.savefig(f"./images/top-{n}-fastest.png")
    plt.show()


def side_plot_quries_together_for_each_command(data, save=False, save_name=None):
    seed = math.floor(random.random() * (random.random() * 1000))
    random.seed(seed)

    unique_hues = data["query"].unique()

    def generate_random_color():
        return (random.random(), random.random(), random.random())

    num_elements = len(unique_hues)
    random_colors = [generate_random_color() for _ in range(num_elements)]

    new_df = data[["command", "median", "query"]]
    sorted_df = new_df.sort_values("command", ascending=False)
    df_no_duplicates = sorted_df.drop_duplicates()
    df_result = df_no_duplicates.pivot(
        index="command", columns="query", values="median"
    )

    def sort(value):
        return value.sort_values(ascending=True)

    def custom_sort(command):
        if command == "baseline":
            return -1  # Return -1 for 'baseline' to ensure it comes first
        else:
            parts = command.split("_")  # Split the command into parts
            numerical_parts = [
                int(part) if part.isdigit() else 0 for part in parts
            ]  # Extract numerical parts and convert to integers
            return sum(numerical_parts)

    df_result = df_result.reindex(
        sorted(df_result.index, key=custom_sort, reverse=True)
    )

    if save:
        plt.figure(figsize=(19.20, 10.80))

    ax = df_result.plot(kind="barh", stacked=True, color=random_colors, legend=False)
    ax.set_yticks(range(len(df_result.index)))
    ax.set_yticklabels(df_result.index)
    ax.set_ylabel("")

    if save:
        plt.savefig(
            (
                f"./images/{save_name}/span-queries-seed-{seed}.eps"
                if save_name
                else f"./images/span-queries-seed-{seed}.eps"
            ),
            format="eps",
            bbox_inches="tight",
        )
        return
    plt.show()


def plot_amount_better_for_each_command(df, save=False):
    df["median_below_stddev"] = df["median"] * 0.9
    # df["median_above_stddev"] = df["median"] + df["stddev"]
    baseline = df[(df["command"] == "baseline")]
    filter_data = df[(df["command"] != "baseline")]
    merged_df = pd.merge(
        filter_data,
        baseline[["query", "median_below_stddev"]],
        on="query",
        suffixes=("_filter", "_baseline"),
    )

    better = merged_df[
        merged_df["median_below_stddev_filter"]
        < merged_df["median_below_stddev_baseline"]
    ]

    count_per_category = better["command"].value_counts()

    count_per_category.plot(kind="bar", color="skyblue", edgecolor="black")

    if save:
        plt.figure(figsize=(12, 8))  # Adjust the width and height as needed
        plt.savefig("./images/amount-commands-better.png")
    else:
        plt.show()


def plot_amount_worse_for_each_command(df, save=False):
    df["median_above_stddev"] = df["median"] * 1.1
    # df["median_above_stddev"] = df["median"] + df["stddev"]
    baseline = df[(df["command"] == "baseline")]
    filter_data = df[(df["command"] != "baseline")]
    merged_df = pd.merge(
        filter_data,
        baseline[["query", "median_above_stddev"]],
        on="query",
        suffixes=("_filter", "_baseline"),
    )

    worse = merged_df[
        merged_df["median_above_stddev_filter"]
        > merged_df["median_above_stddev_baseline"]
    ]

    # worse = filter_data[filter_data["median_above_stddev"] < baseline["median_above_stddev"]]

    count_per_category = worse["command"].value_counts()

    count_per_category.plot(
        kind="bar",
        color="skyblue",
        edgecolor="black",
    )

    plt.figure(figsize=(15, 5))  # Adjust the width and height as needed
    if save:
        plt.figure(figsize=(15, 5))  # Adjust the width and height as needed
        plt.savefig("./images/amount-commands-worse.png")
    else:
        plt.show()


def plot_count_worse_with_better(df, save=False):
    baseline = df[(df["command"] == "baseline")]
    filter_data = df[(df["command"] != "baseline")]

    high_counts = {}
    low_counts = {}
    query_count = {}
    query_extreme = {}
    query_extreme_32 = {}

    for index, data in filter_data.iterrows():
        median = data["median"]
        query = data["query"]
        command = data["command"]
        baseline_query = baseline[baseline["query"] == query].iloc[0].to_dict()

        if median > baseline_query["median"] * 2 and command == "32_32":
            if query in query_extreme_32:
                query_extreme_32[query].append(command)
            else:
                query_extreme_32[query] = [command]

        if median > baseline_query["median"] * 2:
            if query in query_extreme:
                query_extreme[query].append(command)
            else:
                query_extreme[query] = [command]

        if median < baseline_query["median"] * 0.9:
            if command in low_counts:
                low_counts[command] += 1
            else:
                low_counts[command] = 1

        if median > baseline_query["median"] * 1.1:
            if query in query_count:
                query_count[query].append(command)
            else:
                query_count[query] = [command]
            if command in high_counts:
                high_counts[command] += 1
            else:
                high_counts[command] = 1

    sns.barplot(
        low_counts,
        edgecolor="black",
        linestyle="dotted",
        alpha=0.7,
        label="Better",
        dodge=True,
    )
    sns.barplot(
        high_counts,
        edgecolor="black",
        linestyle="dotted",
        alpha=0.7,
        label="Worse",
        dodge=True,
    )

    with open("bad_queries.txt", "w") as file:
        json.dump(query_count, file, indent=2)

    with open("extreme_bad_queries.txt", "w") as file:
        json.dump(query_extreme, file, indent=2)
    with open("extreme_bad_queries_32.txt", "w") as file:
        json.dump(query_extreme_32, file, indent=2)

    # Add a legend and informative axis label
    plt.legend()
    if save:
        plt.figure(figsize=(15, 5))  # Adjust the width and height as needed
        plt.savefig("./images/amount-commands-worse.png")
    else:
        plt.show()


def plot_top_slowest_n_sum(df, n, save=False):
    result = (
        df.groupby("command")["median"]
        .nlargest(n)
        .reset_index(level=1, drop=True)  # Drop the level to remove the duplicate index
        .groupby("command")
        .sum()
        .reset_index()
    )
    sns.barplot(
        data=result,
        x="median",
        y="command",
        color="b",
        edgecolor="black",
        linestyle="dotted",
    )

    plt.legend()
    plt.xlabel("")
    plt.ylabel("")
    if save:
        plt.figure(figsize=(15, 5))  # Adjust the width and height as needed
        plt.savefig("./images/amount-commands-worse.png")
    else:
        plt.show()


def plot_top_fastest_n_sum(df, n, save=False):
    result = (
        df.groupby("command")["median"]
        .nsmallest(n)
        .reset_index(level=1, drop=True)  # Drop the level to remove the duplicate index
        .groupby("command")
        .sum()
        .reset_index()
    )
    sns.barplot(
        data=result,
        x="median",
        y="command",
        color="b",
        edgecolor="black",
        linestyle="dotted",
    )

    plt.legend()
    plt.xlabel("")
    plt.ylabel("")
    if save:
        plt.figure(figsize=(15, 5))  # Adjust the width and height as needed
        plt.savefig("./images/amount-commands-worse.png")
    else:
        plt.show()


def amount_worse_or_better_compared_to_baseline(data, name, save=False, save_name=None):
    baseline = data[(data["command"] == "baseline")]
    config = data[(data["command"] == name)]

    baselines = baseline.sort_values(by="query")["median"]
    results = config.sort_values(by="query")["median"]
    fontsize = 34

    percentage_diffs = []
    for baseline, query_result in zip(baselines, results):
        query_percentage_diff = [(query_result) / baseline]
        percentage_diffs.extend(query_percentage_diff)

    bins = [
        0,
        0.5,
        0.9,
        1.1,
        1.5,
        2,
        np.inf,
    ]
    bin_labels = [
        "> 50% improvement",
        "10% to 50% improvement",
        "Unchanged",
        "10% to 50% degradation",
        "50% to 100% degradation",
        "> 100% degradation",
    ]

    if save:
        plt.figure(figsize=(19.20, 10.80))
    # Group percentage differences into bins
    binned_diffs = np.digitize(percentage_diffs, bins, right=True)

    # Count occurrences of each bin
    unique_bins, counts = np.unique(binned_diffs, return_counts=True)

    # Create a bar plot using Seaborn
    active_bin_labels = []
    for unique_bin in unique_bins:
        active_bin_labels.append(bin_labels[unique_bin - 1])

    # Create a bar plot using Seaborn
    sns.barplot(x=unique_bins, y=counts[counts > 0], color="skyblue")

    # Customize plot labels and title
    plt.xlabel("", fontsize=fontsize)
    plt.ylabel("Number of queries", fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.title("Distribution of Results Compared to Baseline", fontsize=fontsize)

    # Rotate x-axis labels for better readability
    plt.xticks(
        ticks=range(len(active_bin_labels)),
        labels=active_bin_labels,
        rotation=45,
        ha="right",
        fontsize=fontsize,
    )

    # Show the plot

    if save:
        plt.savefig(
            (
                f"./images/{save_name}/amount-worse-and-better.eps"
                if save_name
                else f"./images/amount-worse-and-better-{name}.eps"
            ),
            format="eps",
            bbox_inches="tight",
        )
        return
    plt.show()


def count_worse_or_better_compared_to_baseline(data, name, save=False, save_name=None):
    baseline = data[(data["command"] == "baseline")]
    config = data[(data["command"] == name)]

    baselines = baseline.sort_values(by="query")["median"]
    results = config.sort_values(by="query")["median"]
    fontsize = 34

    percentage_diffs = []
    for baseline, query_result in zip(baselines, results):
        query_percentage_diff = [(query_result - baseline) / baseline * 100]
        percentage_diffs.extend(query_percentage_diff)

    # Create a bar plot using Seaborn
    bins = [-np.inf, 0, np.inf]
    bin_labels = ["Slower", "Faster"]

    if save:
        plt.figure(figsize=(19.20, 10.80))
    # Group percentage differences into bins
    binned_diffs = np.digitize(percentage_diffs, bins, right=True)

    # Count occurrences of each bin
    unique_bins, counts = np.unique(binned_diffs, return_counts=True)

    # Create a bar plot using Seaborn
    sns.barplot(x=unique_bins, y=counts, color="skyblue")

    # Customize plot labels and title
    plt.xlabel("", fontsize=fontsize)
    plt.ylabel("Count", fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.title("Amount slower vs faster", fontsize=fontsize)

    # Rotate x-axis labels for better readability
    plt.xticks(
        ticks=range(len(bin_labels)),
        labels=bin_labels,
        rotation=45,
        ha="right",
        fontsize=fontsize,
    )

    # Show the plot

    if save:
        plt.savefig(
            (
                f"./images/{save_name}/count-worse-and-better.eps"
                if save_name
                else f"./images/{name}/count-worse-and-better.eps"
            ),
            format="eps",
            bbox_inches="tight",
        )
        return
    plt.show()


def side_plot_quries_together_for_each_command_without_n_fastest_and_slowest(
    data, n, save=False
):

    baseline_group = data[data["command"] == "baseline"]
    largest_values = baseline_group.nlargest(n, "median")
    smallest_values = baseline_group.nsmallest(n, "median")

    largest_queries = largest_values["query"]
    smallest_queries = smallest_values["query"]

    filtered_data = data[
        ~(
            (data["query"].isin(largest_queries))
            | (data["query"].isin(smallest_queries))
        )
    ]

    seed = math.floor(random.random() * (random.random() * 1000))
    random.seed(seed)

    unique_hues = filtered_data["query"].unique()

    def generate_random_color():
        return (random.random(), random.random(), random.random())

    num_elements = len(unique_hues)
    random_colors = [generate_random_color() for _ in range(num_elements)]

    new_df = filtered_data[["command", "median", "query"]]
    sorted_df = new_df.sort_values("command", ascending=False)
    df_no_duplicates = sorted_df.drop_duplicates()
    df_result = df_no_duplicates.pivot(
        index="command", columns="query", values="median"
    )

    def custom_sort(command):
        if command == "baseline":
            return -1  # Return -1 for 'baseline' to ensure it comes first
        else:
            parts = command.split("_")  # Split the command into parts
            numerical_parts = [
                int(part) if part.isdigit() else 0 for part in parts
            ]  # Extract numerical parts and convert to integers
            return sum(numerical_parts)

    df_result = df_result.reindex(
        sorted(df_result.index, key=custom_sort, reverse=True)
    )

    if save:
        plt.figure(figsize=(19.20, 10.80))

    ax = df_result.plot(kind="barh", stacked=True, color=random_colors, legend=False)
    ax.set_yticks(range(len(df_result.index)))
    ax.set_yticklabels(df_result.index)
    ax.set_ylabel("")

    if save:
        plt.savefig(
            f"./images/span-queries-seed-{seed}.eps", format="eps", bbox_inches="tight"
        )
        return
    plt.show()


def generate_attachments(data, base_folder_path):
    directories = [
        d
        for d in os.listdir(base_folder_path)
        if os.path.isdir(os.path.join(base_folder_path, d))
    ]
    for dir in directories:
        dir_name = f"./images/attachments/{dir}"
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        move_from = f"{base_folder_path}{dir}"
        move_to = f"{dir_name}/raw_data"
        shutil.copytree(move_from, move_to)

        if dir == "baseline":
            continue
        save_name = f"attachments/{dir}"
        amount_worse_or_better_compared_to_baseline(data, dir, True, save_name)
        plt.clf()
        query_data = create_compare_df(data, dir)
        side_plot_all(query_data, True, save_name)
        plt.clf()
    side_plot_quries_together_for_each_command(all_commands, True, "attachments")


def shortn_command_name(name):
    numbers = re.findall(r"\d+", name)

    # Convert the extracted numbers from strings to integers
    numbers = list(numbers)
    return "_".join(numbers)


data_dir = "./results/tests/thesis/"
all_commands = get_all_command_variants(data_dir, shortn_command_name)


name = "32_32_50"
data = create_compare_df(all_commands, name)

# generate_attachments(all_commands, data_dir)

# side_plot_quries_together_for_each_command(all_commands, True)
amount_worse_or_better_compared_to_baseline(all_commands, name, True)
# count_worse_or_better_compared_to_baseline(all_commands, name, True)
# # side_plot_all(data, True, name)
# side_plot_quries_together_for_each_command_without_n_fastest_and_slowest(
#     all_commands, 20
# )
# side_plot_top_n_fastest(data, 20)
# side_plot_top_n_slowest(data, 20)
# plot_count_worse_with_better(all_commands)
# plot_top_slowest_n_sum(all_commands, 20)
# plot_top_fastest_n_sum(all_commands, 20)
