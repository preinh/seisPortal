#!/bin/bash
D="-d postgresql://sysop:sysop@10.110.0.130/sc_master"

for evt in $(scevtls $D --begin "2000-01-01 00:00:00" --end  "2020-01-01 00:00:00" ); do
	echo "processing evt: " $evt 
	[[ ! -f  $evt.1.png ]] && scxmldump $D -E $evt | scmapcut --ep - -E $evt -d 300x200 -m  1 --layers -o $evt.1.png
	[[ ! -f  $evt.5.png ]] && scxmldump $D -E $evt | scmapcut --ep - -E $evt -d 300x200 -m  5 --layers -o $evt.5.png
	[[ ! -f $evt.25.png ]] && scxmldump $D -E $evt | scmapcut --ep - -E $evt -d 300x200 -m 25 --layers -o $evt.25.png
done
