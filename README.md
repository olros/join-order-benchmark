# Join-Order-Benchmark

This package contains the Join Order Benchmark (JOB) queries from:
"[How Good Are Query Optimizers, Really?](http://www.vldb.org/pvldb/vol9/p204-leis.pdf)"
by Viktor Leis, Andrey Gubichev, Atans Mirchev, Peter Boncz, Alfons Kemper, Thomas Neumann
PVLDB Volume 9, No. 3, 2015


The `csv_files/schematext.sql` and `queries/*.sql` are modified to MySQL syntax.


## Quick Start

1. Obtain the data:
```shell
cd csv_files/
wget http://homepages.cwi.nl/~boncz/job/imdb.tgz
tar -xvzf imdb.tgz
```

2. Launch the database server.
3. Create IMDb tables in MySQL:

```sqlmysql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-create-tables.sql
```

4. Load data using this script in MySQL, 1-by-1 to avoid a corrupt database if errors happen.
```sqlmysql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-load-data-1.sql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-load-data-2.sql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-load-data-3.sql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-load-data-4.sql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-load-data-5.sql
```

Copy the data-directory between each command to allow rollback if errors occur. The data-directory to make a copy of is:
`/build/mysql-test/var/mysqld.1/data`

5. Add indexes to the IMDb database in MySQL
```sqlmysql
mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/imdb-index-tables.sql
```

## Order Problem

Please note that `queries/17b.sql` and `queries/8d.sql` may exhibit order issues due to the use of different order rules from MySQL. This is not a real bug.

## Improving TiDB Performance using Analyze Table
Please execute analyze_table.sql to optimize the TiDB performance.