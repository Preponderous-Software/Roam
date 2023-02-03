# clear .json files in data directory
rm -f data/*.json
rm -f data/rooms/*.json

# clear png files in roompngs directory
rm -f roompngs/*.png

# rename existing mapImage.png
date=$(date +%Y%m%d%H%M%S)
mv mapImage.png mapImage_$date.png