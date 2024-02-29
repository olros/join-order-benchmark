import glob
import json
import math
import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

folder_path = "./results/tests/base_tests/"
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


dfs = [
    pd.json_normalize(query["results"], sep="_").assign(
        query=query["query"], query_number=query["query_number"]
    )
    for query in data
]

df = pd.concat(dfs, ignore_index=True)


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


df = df.sort_values(by=["query"], key=lambda x: x.apply(custom_sort))


sns.set_theme()

colors = {"with_reoptimization": "blue", "without_reoptimization": "lightgreen"}

hue_order = ["with_reoptimization", "without_reoptimization"]


def plot_all(save=False):
    split_dfs, num_rows, num_cols = split_df(df)

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(15, 5 * num_rows))
    axes = axes.flatten()
    for i, (part_df, ax) in enumerate(zip(split_dfs, axes)):
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


def plot_query(query_num, save=False):
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


def plot_query_range(lower, upper, save=False):
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


def plot_all_no_split(save=False):
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
        plt.savefig(f"./images/data-query-{lower}-to-{upper}.png")
    plt.show()


def plot_group_by_without_time(save=False):
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


def side_plot_all(save=False):
    df_without = df[df["command"] == "without_reoptimization"]
    df_with = df[df["command"] == "with_reoptimization"]

    df_with = df_with.sort_values(by=["query"], key=lambda x: x.apply(custom_sort))
    df_without = df_without.sort_values(
        by=["query"], key=lambda x: x.apply(custom_sort)
    )
    new_df = pd.merge(df_with, df_without, on="query", suffixes=("_with", "_without"))

    sorted_df = new_df.sort_values(by="median_without")
    split_dfs, num_rows, num_cols = split_df(sorted_df)

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(15, 5 * num_rows))
    axes = axes.flatten()
    for i, (part_df, ax) in enumerate(zip(split_dfs, axes)):
        sns.set_color_codes("pastel")
        sns.barplot(
            x="median_without",
            y="query",
            data=part_df,
            color="b",
            ax=ax,
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
            data=part_df,
            color="b",
            ax=ax,
            legend=False,
            label="With",
            alpha=0.7,
            edgecolor="black",
        )
        bar.set_xlabel("Median seconds")

    # Add a legend and informative axis label
    sns.despine(left=True, bottom=True)
    handles, labels = axes[0].get_legend_handles_labels()
    unique_labels = list(set(labels))
    combined_handles = [handles[labels.index(label)] for label in unique_labels]
    fig.legend(combined_handles, unique_labels, ncol=2, loc="lower right", frameon=True)

    if save:
        plt.savefig("./images/all-data-sorted.png")
    plt.show()


def side_plot_quey(query_num, save=False):
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


def side_plot_queries(query_nums, save=False):
    query_df = df[df["query_number"].isin(query_nums)]
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


def side_plot_top_n_slowest(n, save=False):
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


def side_plot_top_n_fastest(n, save=False):
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


def side_plot_quries_together_for_each_command(data, save=False):
    np.random.seed(42)

    unique_hues = data["query"].unique()

    def generate_random_rgb():
        return (random.random(), random.random(), random.random())

    num_elements = len(unique_hues)
    random_colors = [generate_random_rgb() for _ in range(num_elements)]

    new_df = data[["command", "median", "query"]]
    sorted_df = new_df.sort_values("median", ascending=False)
    df_no_duplicates = sorted_df.drop_duplicates()
    df_result = df_no_duplicates.pivot(index="command", columns="query", values="median")

    ax = df_result.plot(kind="barh", stacked=True, color=random_colors, legend=False)
    ax.set_yticks(range(len(df_result.index)))
    ax.set_yticklabels(df_result.index)

    if save:
        plt.savefig("./images/span-queries.png")
    plt.show()


def get_all_command_variants(base_folder_path):
    directories = [
        d
        for d in os.listdir(base_folder_path)
        if os.path.isdir(os.path.join(base_folder_path, d))
    ]
    data = []
    for i, dir in enumerate(directories):
        json_files = glob.glob(os.path.join(f"{base_folder_path}{dir}", "*.json"))
        for json_file in json_files:
            name = json_file.split("/")[-1].replace(".json", "")
            with open(json_file, "r") as file:
                if os.path.getsize(json_file) != 0:
                    json_data = json.load(file)
                    if len(json_data["results"]) < 2:
                        continue
                    json_data["query"] = f"{name}"
                    json_data["query_number"] = int(get_query_number(name))
                    json_data["results"][1]["command"] = f"{dir}"
                    if i != 0:
                        json_data["results"] = [json_data["results"][1]]
                    else:
                        json_data["results"][0]["command"] = "Baseline"

                    data.append(json_data)
    dfs = [
        pd.json_normalize(query["results"], sep="_").assign(
            query=query["query"], query_number=query["query_number"]
        )
        for query in data
    ]

    return pd.concat(dfs, ignore_index=True)


all_commands = get_all_command_variants("./results/tests/")
side_plot_quries_together_for_each_command(all_commands)
