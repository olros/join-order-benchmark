#!/bin/bash
set -e

TASKNUM=5
trap "exec 1000>&-;exec 1000<&-;exit 0" 2
tempfifo=$$.fifo 
mkfifo $tempfifo
exec 1000<>$tempfifo
rm -rf $tempfifo

for ((i=1; i<=$TASKNUM; i++))
do
    echo >&1000
done

load_data() {
  CURDIR=$(cd `dirname $0`; pwd)
  PREFIX=$CURDIR/csv_files/
  
  # ~/Documents/GitHub/mysql-server/build/bin/mysql --local-infile=1 -u root -S /Users/olafrosendahl/Documents/GitHub/mysql-server/build/mysql-test/var/tmp/mysqld.1.sock -D imdbload < $PREFIX/schematext.sql
  # ~/Documents/GitHub/mysql-server/build/bin/mysql --local-infile=1 -u root -S /Users/olafrosendahl/Documents/GitHub/mysql-server/build/mysql-test/var/tmp/mysqld.1.sock -D imdbload < $PREFIX/fkindexes.sql
  
  for csv_file in `ls $CURDIR/csv_files/*.csv`; do
    read -u1000

    bname=${csv_file%.*}
    sql_file="$bname.sql"
    table=${bname#$PREFIX}
    sql="LOAD DATA LOCAL INFILE '$csv_file' INTO TABLE $table FIELDS TERMINATED BY ',';"
    echo $sql > $sql_file
    echo $sql_file
    {
      #  ~/Documents/GitHub/mysql-server/build/bin/mysql --local-infile=1 -u root -S /Users/olafrosendahl/Documents/GitHub/mysql-server/build/mysql-test/var/tmp/mysqld.1.sock -D imdbload < $sql_file
       echo >&1000
    }& 
  done
}

load_data
wait
echo "done!!!!!!!!!!"
