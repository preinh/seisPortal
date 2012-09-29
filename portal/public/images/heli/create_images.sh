#!/bin/bash
D="-d postgresql://sysop:sysop@10.110.0.130/sc_master"
I='-I "combined://seisrequest.iag.usp.br:18000;seisrequest.iag.usp.br:18001"'
H="-H localhost:4803"
H="-H 10.110.1.132:4803"

#for stream in $( python get_streams.py ); do
for stream in $( cat streams.lst ); do
	echo "processing stream: " $stream 
	scheli capture --offline -I "combined://seisrequest.iag.usp.br:18000;seisrequest.iag.usp.br:18001" \
		 --amp-range=1E3 --stream $stream -N -o $stream.png
done


