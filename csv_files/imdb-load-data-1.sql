SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/aka_name.csv' INTO TABLE aka_name FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/aka_title.csv' INTO TABLE aka_title FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/cast_info.csv' INTO TABLE cast_info FIELDS TERMINATED BY ',';
