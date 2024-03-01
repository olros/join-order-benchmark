#!/bin/bash
set -e

CURDIR=$(cd `dirname $0`; pwd)
OUTDIR=$CURDIR/results/tests/

if [ ! -e $OUTDIR ]; then
  mkdir -p $OUTDIR
fi

cd $CURDIR

NC='\033[0m' 
BIWhite='\033[1;97m'

mysql_client="~/Documents/GitHub/mysql-server/build-release/bin/mysql"
mysql_sock="/Users/olafrosendahl/Documents/GitHub/mysql-server/build-release/mysql-test/var/tmp/mysqld.1.sock"

export mysql_connect="$mysql_client -u root -S $mysql_sock -D imdbload -t"

eval "$mysql_connect<<eof
UPDATE mysql.engine_cost SET cost_value = 0.25 WHERE cost_name = 'io_block_read_cost';
UPDATE mysql.engine_cost SET cost_value = 0.25 WHERE cost_name = 'memory_block_read_cost';
FLUSH OPTIMIZER_COSTS;

SET PERSIST innodb_stats_persistent = 1;
SET PERSIST innodb_stats_auto_recalc = 0;

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

thresholds=("16" "24" "32" "40" "48")

threshold_pairs=()

threshold_pairs+=("-1 -1") # Mapped to run without re-optimization

for threshold_below in "${thresholds[@]}"; do
  for threshold_above in "${thresholds[@]}"; do
    threshold_pairs+=("$threshold_below $threshold_above")
  done
done

for threshold in "${threshold_pairs[@]}"; do
  read -r below above <<< "$threshold"

  if [ $below -eq "-1" ] && [ $above -eq "-1" ]
  then
    echo -e "${BIWhite}Starting benchmarking for baseline${NC}"
    run_reopt=false
    output_folder="${OUTDIR}baseline/"
  else
    echo -e "${BIWhite}Starting benchmarking with thresholds: below: $below, above: $above${NC}"
    run_reopt=true
    output_folder="${OUTDIR}below_${below}_above_${above}/"
  fi

  if [ ! -e $output_folder ]; then
    mkdir -p $output_folder
  fi

  for file in `ls queries/*.sql`; do
    bname=`basename $file`
    name=${bname%.*}
    outputmarkdown=$output_folder/$name.md
    outputjson=$output_folder/$name.json
    echo -e "${BIWhite}+-------------+${NC}"
    echo -e "${BIWhite}| Run $name.sql |${NC}"
    echo -e "${BIWhite}+-------------+${NC}"

    original_query=$(<$file)
    query=${original_query/";"/"\G"}
    if [ $run_reopt == true ]
    then
      query=${query/"SELECT "/"SELECT /*+ SET_VAR(sql_buffer_result=1) RUN_REOPT($below, $above) */ "}
    else
      query=${query/"SELECT "/"SELECT /*+ SET_VAR(sql_buffer_result=1) */ "}
    fi

    if [ -s "$outputjson" ]
    then
      echo "Results for $name already collected, skipping..."
      continue
    fi

    hyperfine \
      --prepare "eval $analyze" \
      --warmup 2 \
      -r 10 \
      --export-json $outputjson \
      --export-markdown $outputmarkdown \
      -n "job" "$mysql_connect -e \"$query\""
  done
done
