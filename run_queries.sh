#!/bin/bash
set -e

CURDIR=$(cd `dirname $0`; pwd)
OUTDIR=$CURDIR/results/tests/

if [ ! -e $OUTDIR ]; then
  mkdir -p $OUTDIR
fi

cd $CURDIR

mysql_client="~/Documents/GitHub/mysql-server/build-release/bin/mysql"
mysql_sock="/Users/olafrosendahl/Documents/GitHub/mysql-server/build-release/mysql-test/var/tmp/mysqld.1.sock"

export mysql_connect="$mysql_client -u root -S $mysql_sock -D imdbload -t"

eval "$mysql_connect<<eof
UPDATE mysql.engine_cost SET cost_value = 0.25 WHERE cost_name = 'io_block_read_cost';
UPDATE mysql.engine_cost SET cost_value = 0.25 WHERE cost_name = 'memory_block_read_cost';
FLUSH OPTIMIZER_COSTS;

SET PERSIST innodb_stats_persistent = 1;
SET PERSIST innodb_stats_auto_recalc = 0;
-- SET PERSIST innodb_stats_persistent = 0;

SET GLOBAL optimizer_switch='hypergraph_optimizer=on';
eof"

analyze="$mysql_connect<<eof
ANALYZE TABLE aka_name;
ANALYZE TABLE aka_title;
ANALYZE TABLE cast_info;
ANALYZE TABLE char_name;
ANALYZE TABLE company_name;
ANALYZE TABLE company_type;
ANALYZE TABLE comp_cast_type;
ANALYZE TABLE complete_cast;
ANALYZE TABLE info_type;
ANALYZE TABLE keyword;
ANALYZE TABLE kind_type;
ANALYZE TABLE link_type;
ANALYZE TABLE movie_companies;
ANALYZE TABLE movie_info;
ANALYZE TABLE movie_info_idx;
ANALYZE TABLE movie_keyword;
ANALYZE TABLE movie_link;
ANALYZE TABLE name;
ANALYZE TABLE person_info;
ANALYZE TABLE role_type;
ANALYZE TABLE title;
eof"

for file in `ls queries/*.sql`; do
  bname=`basename $file`
  name=${bname%.*}
  outputmarkdown=$OUTDIR/$name.md
  outputjson=$OUTDIR/$name.json
  echo "Run $file"

  original_query=$(<$file)
  export query=${original_query/";"/"\G"}
  export query_without_reoptimization=${query/"SELECT "/"SELECT /*+ SET_VAR(sql_buffer_result=1) */ "}
  export query_with_reoptimization=${query/"SELECT "/"SELECT /*+ SET_VAR(sql_buffer_result=1) RUN_REOPT */ "}

  function without_reoptimization {
    eval "$mysql_connect<<eof
$query_without_reoptimization
eof"
}
  function with_reoptimization {
    eval "$mysql_connect<<eof
$query_with_reoptimization
eof"
}
  export -f without_reoptimization
  export -f with_reoptimization

  hyperfine --prepare "eval $analyze" --warmup 2 -r 10 --export-json $outputjson --export-markdown $outputmarkdown --shell=bash without_reoptimization with_reoptimization
done
