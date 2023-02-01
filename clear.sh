# clear .json files in data directory
rm -f data/*.json
rm -f data/rooms/*.json

# clear png files in roompngs directory
rm -f roompngs/*.png

# rename existing combined.png
date=$(date +%Y%m%d%H%M%S)
mv combined.png combined_$date.png