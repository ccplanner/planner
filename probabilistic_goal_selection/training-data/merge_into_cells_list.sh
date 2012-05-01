cat g | grep "^goal" | sed "s/goal(\([0-9]*\)[, ]*\([0-9]\)) V=\[\([.0-9]*\)\]/\1,\2,g,\3/g" |sort -n > tmp

cat p | awk '{OFS=",";print $1,$2,"p"}' >> tmp
cat e | awk '{OFS=",";print $1,$2,"e"}' >> tmp
cat m | awk '{OFS=",";print $1,$2,"m"}' >> tmp

cat tmp | sort -n > cells.csv

