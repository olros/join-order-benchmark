#!/bin/bash
set -e

CURDIR=$(cd `dirname $0`; pwd)
OUTDIR=$CURDIR/results/$1

if [ ! -e $OUTDIR ]; then
  mkdir -p $OUTDIR
fi

cd $CURDIR

mysql_connect="~/Documents/GitHub/mysql-server/build/bin/mysql -u root -S /Users/olafrosendahl/Documents/GitHub/mysql-server/build/mysql-test/var/tmp/mysqld.1.sock -D imdbload"


for file in `ls queries/*.sql`; do
  file="queries/11a.sql"
  bname=`basename $file`
  name=${bname%.*}
  # outputfile=$OUTDIR/$name.out
  outputfile=$OUTDIR/$name.md
  errorfile=$OUTDIR/$name.err
  echo "Run $file"

  export query=$(<$file)
  export query_with_reoptimization=${query/"SELECT "/"SELECT /*+ RUN_REOPT */ "}

  function without_reoptimization {
    ~/Documents/GitHub/mysql-server/build/bin/mysql -u root -S /Users/olafrosendahl/Documents/GitHub/mysql-server/build/mysql-test/var/tmp/mysqld.1.sock -D imdbload -t<<eof
SET optimizer_switch='hypergraph_optimizer=on';
$query
eof
}
  function with_reoptimization {
    ~/Documents/GitHub/mysql-server/build/bin/mysql -u root -S /Users/olafrosendahl/Documents/GitHub/mysql-server/build/mysql-test/var/tmp/mysqld.1.sock -D imdbload -t<<eof
SET optimizer_switch='hypergraph_optimizer=on';
$query_with_reoptimization
eof
}
  export -f without_reoptimization
  export -f with_reoptimization
  # hyperfine -r 10 --shell=bash without_reoptimization with_reoptimization > $outputfile
  hyperfine --warmup 2 -r 5 --export-markdown $outputfile --shell=bash without_reoptimization with_reoptimization
done
