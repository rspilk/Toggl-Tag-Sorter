#!/usr/bin/env python

#    Toggl Api Grabber - Grabs and sorts toggl data based on tags
#    Copyright (C) 2012 -  Tyler Spilker - Gonzaga University
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


# -- Imports -- #
import urllib2, base64, simplejson, time, optparse,sys,datetime, json

# -- Declaring Global Vars -- #
global username
try:
  username =  ### API TOKEN GOES HERE ###
except:
  print("Error: No Toggl API Token Entered. Line # 26")
  print("You must first edit toggl.py and change 'username = token ### API TOKEN GOES HERE ###' to (example) 'username = 'abc123def456ghi789' ' ")
  print(" ")
  print("The token can be found on the Toggl webiste under the user's Profile")
  sys.exit()
global password 
password = 'api_token'

global midnight 
midnight = "00:00:00"
global currentTime 
currentTime = time.strftime('%H:%M:%S')

global almostMidnight
almostMidnight = "23:59:59"

global currentDate 
currentDate = "20"+time.strftime('%y-%m-%d')

global timeBlank
timeBlank = 0

global dayDict
dayDict = {'Monday':1,'Tuesday':2,'Wednesday':3,'Thursday':4,'Friday':5,'Saturday':6,'Sunday':7}

# -- Command Line Options -- #
OP=optparse.OptionParser(description="Toggl data grabber. Please note that tags may overlap in time, currently only Admin, Ops and tagless are added together to form final total. Accuracy is not ensured if you tag differently than I do",epilog="This program does not scrub inputs yet. Please be careful when entering things. Double check your format to the -h before hitting enter.")

OP.add_option('-d', '--start_date', help="Start Date, default: Current Date. Format: YYYY-MM-DD", dest="startDate", default=currentDate)
OP.add_option('-e', '--end_date', help="End Date, default: Current Date. Format: YYYY-MM-DD", dest="endDate", default=None)
OP.add_option('-t', '--start_time', help="Start Time, default: midnight. Format: HH:MM:SS", dest="startTime", default=midnight)
OP.add_option('-m', '--end_time', help="End Time, default: current time. Format: HH:MM:SS", dest="endTime", default=almostMidnight)
OP.add_option('-1', '--tag1', help="Tag one, defaults to ADMINISTRATIVE, use tags to look for durations in certain areas", dest="tagOne", default="ADMINISTRATIVE")
OP.add_option('-2', '--tag2', help="Tag two, defaults to Meeting, use tags to look for durations in certain areas", dest="tagTwo", default="MEETING")
OP.add_option('-3', '--tag3', help="Tag three, default is Professional Development.", dest="tagThree", default="PROFESSIONAL DEVELOPMENT")
OP.add_option('-4', '--tag4', help="Tag three, default is Operations.", dest="tagFour", default="OPERATIONS")
OP.add_option('-5', '--tag5', help="Tag three, default is None.", dest="tagFive", default=None)
OP.add_option('-q', '--quick', help="Shortcuts for quick/most used commands; Current commands: yesterday, ", dest="quick", default=None)


# -- Parsing passed arguments to variables -- #
options,args=OP.parse_args()

startDate = options.startDate
endDate = options.endDate
startTime = options.startTime
endTime = options.endTime
tagOne = options.tagOne
tagTwo = options.tagTwo
tagThree = options.tagThree
tagFour = options.tagFour
tagFive = options.tagFive

quick = options.quick

# This fixes the issue where the endDate remains the current run date. I need to fix this again as I lost my original code.
if endDate == None:
  endDate = startDate


if quick:                                                                   # This handles if there is a -q passed to it (quick commands)
  def whichDay(dayPassed):                                                  # whichDay determines based on the day entered, how it
    todayExplicit = 0                                                       # relates to the current day. Does the math for you
    global startDate, endDate, startTime, endTime
    day = datetime.date(int(currentDate.split('-')[0]),int(currentDate.split('-')[1]),int(currentDate.split('-')[2]))
    Year,WeekNum,DOW = day.isocalendar()
    if dayPassed.title() == 'Today':
      todayExplicit = 1
      dayDict[dayPassed.title()] = DOW
    try:
      offset = DOW - dayDict[dayPassed.title()]
    except:
      print("You have entered an invalid quick command, please try again")
      sys.exit()
    timeDelta = datetime.timedelta(offset)
    d = datetime.date.today()
    returnDate = d - timeDelta
    startDate = str(returnDate.year)+"-"+str(returnDate.month)+"-"+str(returnDate.day)
    if endDate:
      endDate = str(returnDate.year)+"-"+str(returnDate.month)+"-"+str(returnDate.day)
    startTime = midnight
    endTime = '23:59:59'
    print("Getting time information from "+dayPassed.title())
    if offset == 0 and todayExplicit != 1:
      print("Hey, that's today!")
    if dayPassed == 'saturday' or dayPassed == 'sunday':
      print("You shouldn't be working so hard!")

  def yesterday():                                                          # Just deals with yesterday. Could collapse to whichDay in future I guess
    global startDate, endDate, startTime, endTime
    startDate = "20"+time.strftime('%y-%m-')+str(int(currentDate.split('-')[2])-1)
    endDate = "20"+time.strftime('%y-%m-')+str(int(currentDate.split('-')[2])-1)
    startTime = midnight
    endTime = '23:59:59'
    print("Showing Time for Yesterday")

  quick = str.lower(quick)                                                  # makes passed -q arg into lower case to avoid case confusion
  if quick == 'yesterday':
    yesterday()
  else:
    whichDay(quick)



def splitTime(time):                                                        # splits passed time into list of ['hour','minute','second']
  time = time.split(':')
  return time


def makeURL(startDate, endDate, startTime, endTime):                        # creates the url to pass JSON request to based on date values
  startTime = splitTime(startTime)
  startHour = startTime[0]
  startMinute = startTime[1]
  startSecond = startTime[2]
  
  endTime = splitTime(endTime)
  endHour = endTime[0]
  endMinute = endTime[1]
  endSecond = endTime[2]
    
  json_current_time = "?start_date="+startDate+"T"+startHour+"%3A"+startMinute+"%3A"+startSecond+"-08%3A00"+"&end_date="+endDate+"T"+endHour+"%3A"+endMinute+"%3A"+endSecond+"-08%3A00"
  url = 'https://www.toggl.com/api/v8/time_entries'+json_current_time
#  url = 'https://www.toggl.com/api/v6/time_entries.json'+json_current_time
#  url = 'http://www.toggl.com/api/v3/tasks.json'+json_current_time         # Old v3 of api. How was this still working, wont respond to curl
  return url

def getToggl(username, password, url):                                      # Grabs JSON and formats it
  data = ['']
  header = {'Content-type': 'application/json'}
  req = urllib2.Request(url)
#  req = urllib2.Request(url, data, {"Content-type": "application/json"})   # Old v3 request.
  auth_string = base64.encodestring('%s:%s' % (username, password)).strip()
  req.add_header("Authorization", "Basic %s" % auth_string)
  f = urllib2.urlopen(req)
  response = f.read()
  formatted = simplejson.loads(response)
  return formatted
  
def countHours(togglData):
  Tags = {}
  for entry in togglData:
    tag = str.upper(entry['tags'][0])
    if tag in Tags:                                                         # If the tag exists in the dictionary Tags, append
      if entry['duration'] > 0:
        if tag == '':
          Tags['TAGLESS'] += entry['duration']
        else:
          Tags[tag] += entry['duration']
      else:
        durEpoch = float(entry['duration'])
        curEpoch = float(time.strftime('%s'))
        if tag == '':
          Tags['TAGLESS'] += curEpoch + durEpoch
        else:
          Tags[tag] += curEpoch + durEpoch
    else:                                                                   # If the tag doesn't exist in the dictionary Tags, just add it
      if entry['duration'] > 0:
        if tag == '':
          Tags['TAGLESS'] = entry['duration']
        else:
          Tags[tag] = entry['duration']
      else:
        durEpoch = float(entry['duration'])
        curEpoch = float(time.strftime('%s'))
        if tag == '':
          Tags['TAGLESS'] = curEpoch + durEpoch
        else:
          Tags[tag] = curEpoch + durEpoch        
  for tag in Tags:
    Tags[tag] = Tags[tag]/3600.0
  return Tags

def printTimes():                                                           # Prints the times in a format. Not necessary, just allows me to use the time easily
  d = time.strptime(startDate,'%Y-%m-%d')
  doW = datetime.date(d.tm_year,d.tm_mon,d.tm_mday).strftime('%a')
  print(startDate+ " " + doW)
  print("From : "+startDate+" "+startTime)
  print("To   : "+endDate+" "+endTime)
  print("")
  for tag in tagTime:
    print("%.2f"%tagTime[tag]+" : Total "+tag+" Time")
  print("%.2f"%totalTime+" : Total Duration")
  print("--------------------------------")
  
  
# -- Run the program. Im sure there is a nicer way of doing this maybe? -- #

togglData = getToggl(username,password, makeURL(startDate, endDate, startTime, endTime))
if togglData == None:
  print "No data recorded between "+startDate+" "+startTime+" and "+endDate+" "+endTime
  print("--------------------------------")
else:
  tagTime = countHours(togglData)
  totalTime = 0.0
  for entry in tagTime:
    totalTime += tagTime[entry]
  printTimes()




# Testing stuff #
#print json.dumps(getToggl(username, password,makeURL(startDate, endDate, startTime, endTime)), separators=(',',':'), indent=4, sort_keys=True)
#print getToggl(username, password,makeURL(startDate, endDate, startTime, endTime))
#print makeURL(startDate, endDate, startTime, endTime)

