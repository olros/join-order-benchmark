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

for file in `ls results/tests/*.md`; do
  bname=`basename $file`
  name=${bname%.*}
  

  file_content=$(<$file)


  without_reoptimization_mean=$(echo "$file_content" | awk 'NR==3 {print $4}')
  with_reoptimization_mean=$(echo "$file_content" | awk 'NR==4 {print $4}')

  result=$(awk -v a="$without_reoptimization_mean" -v b="$with_reoptimization_mean" 'BEGIN {if (a > b) print "✅"; else if (a < b) print "❌"; else print "≈"}')

  echo "## $name $result" >> "$output_file"
  echo "" >> "$output_file"
  echo "$file_content" >> "$output_file"
  echo "" >> "$output_file"

done
