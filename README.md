# Join-Order-Benchmark

> Based on [https://github.com/winkyao/join-order-benchmark](https://github.com/winkyao/join-order-benchmark)

This package contains the Join Order Benchmark (JOB) queries from:
"[How Good Are Query Optimizers, Really?](http://www.vldb.org/pvldb/vol9/p204-leis.pdf)"
by Viktor Leis, Andrey Gubichev, Atans Mirchev, Peter Boncz, Alfons Kemper, Thomas Neumann
PVLDB Volume 9, No. 3, 2015

The `csv_files/imdb-create-tables.sql` and `queries/*.sql` are modified to MySQL syntax.

## Quick Start

1. Obtain the data:
```shell
cd csv_files/
wget http://homepages.cwi.nl/~boncz/job/imdb.tgz
tar -xvzf imdb.tgz
```

1. Launch the database server and connect (with local-infile turned on in the database server)
2. Create IMDb tables in MySQL:

```sqlmysql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-create-tables.sql
```

4. Load data in MySQL:
```sqlmysql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-load-data.sql
```

5. Add indexes to the IMDb database in MySQL
```sqlmysql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-index-tables.sql
```

Copy the data-directory afterwards to allow restoring the database data without loading it again if necessary. The data-directory to make a copy of is:
`/build/mysql-test/var/mysqld.1/data`

## Running the queries

We use [hyperfine](https://github.com/sharkdp/hyperfine) as a benchmarking-tool to measure the queries, you'll therefore need to install it before running the queries. To run all queries, run the following in your terminal:

```bash
./run_queries.sh
```

This will run the queries in the [queries-folder](./queries/) one-by-one, first without re-optimization, and then with re-optimization using different variables for the re-optimization hint. The results are outputted to different folders in the [results-folder](./results/tests/) as json-files for each query. You'll be able to see the progress in the terminal as the queries are being executed.

### Run single query

You can also run a single query without and with re-optimization by running the following in your terminal, replace `<query>` with the name of the query you want to run:

```sh
./run_query.sh <query>
```

The result wil be outputted to a file in the [results-folder](./results/tests/) as a json-file and will also be visible in the terminal.

### Order Problem

Please note that `queries/17b.sql` and `queries/8d.sql` may exhibit order issues due to the use of different order rules from MySQL. This is not a real bug.

## Analyze results

We've created a Python-script with lots of different methods for visualizing the results in [`visulize-info.py`](./visulize-info.py). Open it to chose which results you want visualized and before running it.
