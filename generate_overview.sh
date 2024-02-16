#!/bin/bash
set -e

CURDIR=$(cd `dirname $0`; pwd)
OUTDIR=$CURDIR/results/

if [ ! -e $OUTDIR ]; then
  mkdir -p $OUTDIR
fi

cd $CURDIR
output_file=$OUTDIR/overview.md

echo "# Overview" > "$output_file"

declare -i improve_count=0
declare -i worse_count=0
declare -i same_count=0

for file in `ls results/tests/*.md`; do
  bname=`basename $file`
  name=${bname%.*}
  
  file_content=$(<$file)

  without_reoptimization_mean=$(echo "$file_content" | awk 'NR==3 {print $4}')
  without_reoptimization_relative=$(echo "$file_content" | awk 'NR==3 {print $12}')
  with_reoptimization_mean=$(echo "$file_content" | awk 'NR==4 {print $4}')
  with_reoptimization_relative=$(echo "$file_content" | awk 'NR==4 {print $12}')

  if [ $(bc <<< "$without_reoptimization_relative >= 1.1") -eq 1 ]
  then
    result="✅"
    improve_count+=1
  elif [ $(bc <<< "$with_reoptimization_relative >= 1.1") -eq 1 ]
  then
    result="❌"
    worse_count+=1
  else
    result="≈"
    same_count+=1
  fi

  echo "## $name $result" >> "$output_file"
  echo "" >> "$output_file"
  echo "$file_content" >> "$output_file"
  echo "" >> "$output_file"

done

echo "Improved: $improve_count, worse: $worse_count, same: $same_count"
