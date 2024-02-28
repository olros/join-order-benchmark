import glob
import json
import math
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

folder_path = "./data/tests/"
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


df = df.sort_values(by=["query"], key=lambda x: x.apply(custom_sort))


sns.set_theme()

colors = {"with_reoptimization": "blue", "without_reoptimization": "lightgreen"}

hue_order = ["with_reoptimization", "without_reoptimization"]


def plot_all(save=False):
    splits = math.ceil(len(df) / 20)

    total_rows = len(df)
    rows_per_part = math.ceil(total_rows / splits)

    split_dfs = [
        df.iloc[i * rows_per_part : (i + 1) * rows_per_part] for i in range(splits)
    ]

    num_rows = math.ceil(splits / 3)
    num_cols = min(splits, 3)
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


def plot_group_by_without_time(save=False):
    df_without = df[df["command"] == "without_reoptimization"]
    df_with = df[df["command"] == "with_reoptimization"]

    df_with = df_with.sort_values(by=["query"], key=lambda x: x.apply(custom_sort))
    df_without = df_without.sort_values(
        by=["query"], key=lambda x: x.apply(custom_sort)
    )

    new_df = pd.merge(df_with, df_without, on="query", suffixes=("_with", "_without"))

    sorted_df = new_df.sort_values(by="median_without")

    splits = math.ceil(len(sorted_df) / 20)

    total_rows = len(sorted_df)
    rows_per_part = math.ceil(total_rows / splits)

    split_dfs = [
        sorted_df.iloc[i * rows_per_part : (i + 1) * rows_per_part]
        for i in range(splits)
    ]

    num_rows = math.ceil(splits / 3)
    num_cols = min(splits, 3)
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(15, 5 * num_rows))
    axes = axes.flatten()
    for part_df, ax in zip(split_dfs, axes):
        bar = sns.barplot(
            data=part_df,
            x="query",
            y="median_without",
            edgecolor="black",
            legend=False,
            color=colors["without_reoptimization"],
            ci=None,
            alpha=0.5,
            ax=ax,
        )
        sns.barplot(
            data=part_df,
            x="query",
            y="median_with",
            edgecolor="black",
            color=colors["with_reoptimization"],
            legend=False,
            ci=None,
            alpha=0.5,
            ax=ax,
        )
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
        plt.savefig("./images/all-data-sorted.png")
    plt.show()


print(df["median"].sum())
plot_group_by_without_time()
