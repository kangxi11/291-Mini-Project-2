#!/bin/sh

sort -u -o terms.txt terms.txt
sort -u -o emails.txt emails.txt
#sort -u -o dates.txt dates.txt
#sort -u -o recs.txt recs.txt
perl break.pl < terms.txt | db_load -T -t btree te.idx
perl break.pl < emails.txt | db_load -T -t btree em.idx
#perl break.pl < dates.txt | db_load -T -t btree da.idx
#perl break.pl < recs.txt | db_load -T -t hash re.idx

