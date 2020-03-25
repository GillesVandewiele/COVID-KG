for i in 2020-03-13/biorxiv_medrxiv/biorxiv_medrxiv/*.json; do
  echo $i
    ./builder.sh $i
done
