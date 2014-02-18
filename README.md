# Toggl Tag Sorter

## The following might be outdated as I have not re-written the README for the latest revision

This project will allow you to use Toggl to document your time specifically around type of tasks performed.
Prior to heading for a meeting, start Toggl with some description and the tag MEETING and at the end of the day it will
output the length of time you spent in MEETING for the day. If you had multiple meetings, it just adds the relevant times
with the same tag.

## Usage
The program depends on using Toggl with tags that are specific enough to organize your time.
In its current revision, sub tags are not counted in any way. 
At some point in the future I might come up with a way of counting time based on sub tags but for now
this is simply used to determine how many total hours a work day contained and how many hours you spent
doing what tasks.
Use main tags in ALL CAPS for this to work. In my daily usage, I
will tag tasks as ADMINSTRATIVE, OPERATIONS, and MEETING followed by
a more descriptive tag and a description. The descriptions are mostly for reference on the toggl.com website.

My usage allows for me to run the program as a cronjob every evening and
record my daily hours to a text file which I can then access at a later
time.

    ./toggl.py

Additionally, if I need to make a correction to a specific day I can retroactively check my time by passing
the -d 2013-09-02 flag will provide a specific date entry.
(All dates must be delivered in ISO 8601 format of YYYY-MM-DD but time
must be delivered using the flags if it is desired) 
    
Will return the following output (as an example)

    2013-09-02 Mon
    From	:	2013-09-02
    To	:	2013-09-02

    4.13	:	NORMAL OPERATIONS Time
    2.85	:	ADMINISTRATIVE Time
    1.33	:	PROFESSIONAL DEVELOPMENT Time
    8.32	:	Total Duration
    -------------------------------------


Additional dates can be retroactively passed into the script with the -d
argument. There are a number of other flags I had originally planned to
use/develop but have since discarded. This is the standard usage at this
time. That is, to get a full days work. 

The time can also be captured retroactively by scripting a bash for loop
like this:

    NUMDAYS=365
    for i in {$NUMDAYS..1}
    do
        ./toggl.py -d $(date --date="$i days ago" +%Y-%m-%d)
        sleep 5
    done >> output.file

Finally, there is an option to input a start and end date (which still behaves strangely for some time periods. getting
400 errors)

to determine something similar to this:
./toggl -d 2014-01-01 -e 2014-01-31

where -d is start date, -e is end date. The program uses the end date as start date unless otherwise told. Outputing:
    From	:	2014-01-01
    To	    :	2014-01-31
    
    104.15	:	NORMAL OPERATIONS Time
    5.33	:	MEETING Time
    2.00	:	PROJECT Time
    35.02	:	ADMINISTRATIVE Time
    2.00	:	TAGLESS Time
    148.50	:	Total Duration
    -------------------------------------

For total hours worked in the month of Janurary


## Contact
Feel free to contact me about this, just not about solicitations. My 
gmail is tyler.spilker



