#!/bin/sh

sort -u terms.txt
sort -u email.txt
sort -u dates.txt
sort -u recs.txt
perl break.pl < terms.txt
perl break.pl < email.txt
perl break.pl < dates.txt
perl break.pl < recs.txt

