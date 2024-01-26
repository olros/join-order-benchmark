SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/char_name.csv' INTO TABLE char_name FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/comp_cast_type.csv' INTO TABLE comp_cast_type FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/company_name.csv' INTO TABLE company_name FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/company_type.csv' INTO TABLE company_type FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/complete_cast.csv' INTO TABLE complete_cast FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/info_type.csv' INTO TABLE info_type FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/keyword.csv' INTO TABLE keyword FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/kind_type.csv' INTO TABLE kind_type FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/link_type.csv' INTO TABLE link_type FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/movie_companies.csv' INTO TABLE movie_companies FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/movie_info_idx.csv' INTO TABLE movie_info_idx FIELDS TERMINATED BY ',';
