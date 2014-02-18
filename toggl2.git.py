#!/usr/bin/env python2

#    Toggl Api Grabber - Grabs and sorts toggl data based on tags
#    Copyright (C) 2013 -  Tyler Spilker - Gonzaga University
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

import urllib2, base64, simplejson, json, time, argparse, datetime
import config
from decimal import Decimal, Rounded, ROUND_HALF_UP, ROUND_UP

password = '%s:%s' % (config.API_TOKEN, config.API_PASSWORD)
user_agent = config.USER_AGENT
workspace_id = config.WORKSPACE
uid = config.UID
url_base = config.URL_BASE
currentDate = time.strftime('%Y-%m-%d')
entries_per_page = 50.0

# -- Command Line Options -- #
ARG=argparse.ArgumentParser(\
      description="Toggl data grabber. Please note that tags may \
          overlap in time. Accuracy is not ensured if you tag \
          differently than I do",\
      epilog="This program does not scrub inputs yet. Please be careful \
          when entering things. Double check your format to the -h \
          before hitting enter.")

ARG.add_argument('-d', '--start_date', help="Start Date, default: Current Date. Format: YYYY-MM-DD", dest="startDate", default=currentDate)
ARG.add_argument('-e', '--end_date', help="End Date, default: Current Date. Format: YYYY-MM-DD", dest="endDate", default=None)


# -- Parsing passed arguments to variables -- #
args=ARG.parse_args()

startDate = args.startDate
endDate = args.endDate
if endDate == None:
    endDate = startDate




def makeURL(startDate, endDate, workspace_id,user_agent,page_num):
    url = '%sworkspace_id=%s&since=%s&until=%s&user_agent=%s&user_ids=%s&page=%s' % (url_base,workspace_id, startDate, endDate, user_agent, uid, page_num)
    return url

def toggl_api_call(url):
    req = urllib2.Request(url)
    auth_string = password.encode('base64').strip()
    req.add_header("Authorization", "Basic %s" % auth_string)
    f = urllib2.urlopen(req)
    response = f.read()
    formatted = simplejson.loads(response)  
    return formatted

def count_time(togglData):
    Tags = {}
    for entry in togglData:
        tag = ''
        if entry['tags'] == []:
            tag = 'TAGLESS'
        for eachTag in entry['tags']:
            if eachTag.isupper():
                tag = eachTag
        if tag in Tags:
            Tags[tag]['duration'] += entry['dur']
        else:
            Tags[tag] = {}
            Tags[tag]['duration'] = entry['dur']
    if togglData == [] or togglData == None:
        Tags["NO TIME RECORDED"]['duration'] = 0
    return Tags
    
def ms_to_hr(time):
    return Decimal(Decimal(time)/Decimal(1000.0)/Decimal(60.0)/Decimal(60.0)).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)

def line():
  print("-------------------------------------")

def printTimes(counted_time):
  d = time.strptime(startDate,'%Y-%m-%d')
  doW = datetime.date(d.tm_year,d.tm_mon,d.tm_mday).strftime('%a')
  print("%s %s") % (startDate, doW)
  print("From\t:\t%s") % startDate
  print("To\t:\t%s") % endDate
  print("")
  for tag in counted_time:
    print(str(ms_to_hr(counted_time[tag]['duration']))+"\t:\t%s Time") % tag
  print("%s\t:\tTotal Duration") % str(ms_to_hr(totalTime(counted_time)))
  line()

def totalTime(counted_time_dict):
    time = Decimal(0.0)
    for entry in counted_time_dict:
        time += counted_time_dict[entry]['duration']
    return time
        

def pretty_print(jsondata):
    return json.dumps(jsondata, sort_keys=True, indent=4, separators=(',', ': '))

def test_data():
    formatted_url = makeURL(startDate,endDate,workspace_id,user_agent)
    data = toggl_api_call(formatted_url)
    print formatted_url
    print pretty_print(data)
    print count_time(data)
    print ms_to_hr(count_time(data)['NORMAL OPERATIONS']['duration'])

def main():
    formatted_url = makeURL(startDate,endDate,workspace_id,user_agent,1)
    data = toggl_api_call(formatted_url)
    data_list = data['data']
    #print pretty_print(data_list)
    if data['total_count'] > 50:
        pages = Decimal(data['total_count']/entries_per_page).quantize(Decimal('0'),rounding=ROUND_UP)
        for page in xrange(pages-1):
            formatted_url = makeURL(startDate,endDate,workspace_id,user_agent,page+2)
            call = toggl_api_call(formatted_url)
            for each in call['data']:
                data_list.append(each)
    #print pretty_print(data_list)
    counted_time = count_time(data_list)
    #print "counted"
    """
    I need to actually break up the requests. They only do 50 entries per request 
    "total_count":2,
    "per_page":50
    if total_count > 50, divide total_count/50.0 and round up to nearest Int and break it up based on that.
    add up each individual request info here:
    https://github.com/toggl/toggl_api_docs/blob/master/reports/detailed.md
    page: integer, default 1
    """
    printTimes(counted_time)

try:
    main()
except:
    print "Something happened with %s to %s"% (startDate, endDate)


