/*
This script loads normalised IMDb data into IMDb database tables created by
using the script imdb-create-tables.sql.

To use the IMDb scripts:

1) Open MySQL in terminal:
 $ mysql -u root -p --local-infile

2) Create IMDb data base in MySQL:
 mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/imdb-create-tables.sql

3) Load data using this script in MySQL:
 mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/imdb-load-data.sql

4) Add constraints to the IMDb database in MySQL
 mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/imdb-add-constraints.sql

 5) Add indexes to the IMDb database in MySQL
 mysql> SOURCE /Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/imdb-index-tables.sql
 
*/


-- SHOW VARIABLES LIKE "local_infile";
SET GLOBAL local_infile = 1;

-- Load Aliases.tsv into Aliases table
LOAD DATA LOCAL INFILE  '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Aliases.tsv'
INTO TABLE Aliases
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Alias_attributes.tsv into Alias_attributes table
LOAD DATA LOCAL INFILE  '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Alias_attributes.tsv'
INTO TABLE Alias_attributes
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Alias_types.tsv into Alias_types table
LOAD DATA LOCAL INFILE  '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Alias_types.tsv'
INTO TABLE Alias_types
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Directors.tsv into Directors table
LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Directors.tsv'
INTO TABLE Directors
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Writers.tsv into Writers table
LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Writers.tsv'
INTO TABLE Writers
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Episode_belongs_to.tsv into Episode_belongs_to table
LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Episode_belongs_to.tsv'
INTO TABLE Episode_belongs_to
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Names_.tsv into Names_ table
LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Names_.tsv'
INTO TABLE Names_
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Name_worked_as.tsv into Name_worked_as table
LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Name_worked_as.tsv'
INTO TABLE Name_worked_as
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Known_for.tsv into Known_for table
LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Known_for.tsv'
INTO TABLE Known_for
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;
