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

2. Launch the database server and connect
3. Create IMDb tables in MySQL:

```sqlmysql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-create-tables.sql
```

4. Load data in MySQL, one-by-one to allow recovery if an error happens and corrupts database.
```sqlmysql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-load-data-1.sql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-load-data-2.sql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-load-data-3.sql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-load-data-4.sql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-load-data-5.sql
```

Copy the data-directory between each command to allow rollback if an error occur. The data-directory to make a copy of is:
`/build/mysql-test/var/mysqld.1/data`

5. Add indexes to the IMDb database in MySQL
```sqlmysql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-index-tables.sql
```

## Running the queries

We use [hyperfine](https://github.com/sharkdp/hyperfine) as a benchmarking-tool to measure the queries, you'll therefore need to install it before running the queries. To run all queries, run the following in your terminal:

```bash
$ ./run_queries.sh
```

This will run the queries in the [queries-folder](./queries/) one-by-one, both with and without re-optimization, and output the results into the [results-folder](./results/) as both markdown and json-files for each query. You'll be able to see the progress in the terminal as the queries are being executed.

### Order Problem

Please note that `queries/17b.sql` and `queries/8d.sql` may exhibit order issues due to the use of different order rules from MySQL. This is not a real bug.
