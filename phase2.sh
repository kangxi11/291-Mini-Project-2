#!/bin/sh

#sort -u terms.txt
sort -u -o emails.txt emails.txt
#sort -u dates.txt
#sort -u recs.txt
#perl break.pl < terms.txt
perl break.pl < emails.txt | db_load -t btree em.idx
#perl break.pl < dates.txt
#perl break.pl < recs.txt

