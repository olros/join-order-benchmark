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

-- Load Principals.tsv into Principals table
LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Principals.tsv'
INTO TABLE Principals
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Had_role.tsv into Had_role table
LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Had_role.tsv'
INTO TABLE Had_role
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Titles.tsv into Titles table
LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Titles.tsv'
INTO TABLE Titles
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Title_genres.tsv into Title_genres table
LOAD DATA LOCAL INFILE  '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Title_genres.tsv'
INTO TABLE Title_genres
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;

-- Load Title_ratings.tsv into Title_ratings table
LOAD DATA LOCAL INFILE  '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/smaller_dataset/normalized/Title_ratings.tsv'
INTO TABLE Title_ratings
COLUMNS TERMINATED BY '\t'
IGNORE 1 LINES;
