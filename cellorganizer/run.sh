#!/bin/bash

echo "Check local drives for files"
cd $HOME/Desktop
if [ ! -d data ]; then
	echo "Data folder not found, creating folder"
	mkdir -p data/images
	cd data/images

	"Downloading HeLa and 3T3 collections"
	wget -nc http://murphylab.web.cmu.edu/data/Hela/3D/multitiff/cellorganizer_full_image_collection.zip
	unzip cellorganizer_full_image_collection.zip
	rm -fv cellorganizer_full_image_collection.zip
	cd ../..
fi

echo "Running Docker container"
docker run --rm -p 8888:8888 \
	-v $(pwd)/data:/home/murphylab/cellorganizer/local \
	--memory="4g" \
	--cpus=2 \
	-e JUPYTER_LAB_ENABLE=yes \
	murphylab/cellorganizer-jupyter
