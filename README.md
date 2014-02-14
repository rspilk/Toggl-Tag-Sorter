# Toggl Tag Sorter

## The following might be outdated as I have not re-written the README for the latest revision

This project will allow you to use Toggl like me. If you often find
yourself needed to break up your time into tasks but can't be bothered
to look it up each day or to use an interface that isn't as clean and
easy as Toggl, you can use this to accomplish that.

## Usage
The program depends on using Toggl in a fashion which uses main tags.
In its current revision, sub tags are not yet counted in any meaningful
way. Use main tags in ALL CAPS for this to work. In my daily usage, I
will tag tasks as ADMINSTRATIVE, OPERATIONS, and MEETING followed by
a more descriptive tag and a description. I have re-written this
from the previous counting methods with the intent on having all data
reported at some point. 

My usage allows for me to run the program as a cronjob every evening and
record my daily hours to a text file which I can then access at a later
time.

    ./toggl.py

Passing the -d 2013-09-02 flag will provide a specific date entry.
(All dates must be delivered in ISO 8601 format of YYYY-MM-DD but time
must be delivered using the flags if it is desired) 
    
Will return the following output (as an example)

    2013-09-02 Mon
    From : 2013-09-02 00:00:00
    To   : 2013-09-02 23:59:59

    4.13 : NORMAL OPERATIONS Time
    2.85 : ADMINISTRATIVE Time
    1.33 : PROFESSIONAL DEVELOPMENT Time
    8.32 : Total Duration
    -------------------------------------

Additional dates can be retroactively passed into the script with the -d
arguement. There are a number of other flags I had originally planned to
use/develop but have since discarded. This is the standard usage at this
time. That is, to get a full days work. Other commands *work* but I
would not suggest them (multi-day, other time periods, etc).

The time can also be captured retroactively by scripting a bash for loop
like this:

    NUMDAYS=365
    for i in {$NUMDAYS..1}
    do
        ./toggl.py -d $(date --date="$i days ago" +%Y-%m-%d)
        sleep 5
    done >> output.file

I have managed to get this to work for the past two years. Obviously,
the sleep command is to avoid being a huge burden on the Toggl people.

## Contact
Feel free to contact me about this, just not about solicitations. My 
gmail is tyler.spilker



