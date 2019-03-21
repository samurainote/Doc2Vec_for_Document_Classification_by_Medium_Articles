import os
from nlp import *

#ADD THE TAGS TO SCRAPE HERE
# "deep-learning" 18/05-18/08, "artificial-intelligence", "data-science",  "machine-learning", "neural-networks"
tag_list = ["Naturallanguageprocessing", "NLP"]

#ADD THE DATES TO SCRAPE HERE
yearstart = 2016
monthstart = 4
yearstop = 2019
monthstop = 3

#LOOPS THROUGH ALL LISTED-TAGS AND SCRAPES DATA OFF OF MEDIUM/TAG/archive
#SAVES THE FILES TO /TAG_SCRAPES/ IN CSV FORMAT
for tag in tag_list:
    scrape_tag(tag, yearstart, monthstart, yearstop, monthstop)
    print("Done with tag: ", tag)

print("done")
