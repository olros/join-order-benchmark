SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/person_info.csv' INTO TABLE person_info FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/role_type.csv' INTO TABLE role_type FIELDS TERMINATED BY ',';

LOAD DATA LOCAL INFILE '/Users/olafrosendahl/Documents/GitHub/join-order-benchmark/csv_files/title.csv' INTO TABLE title FIELDS TERMINATED BY ',';
