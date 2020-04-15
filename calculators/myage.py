#!/usr/bin/env python
import datetime
from dateutil import relativedelta
person = {
	"name" : "Laith Alissa",
	"year" : 1991,
	"month" : 8,
	"day" : 4
}
dob = datetime.date(
	person['year'],
	person['month'], 
	person['day']
)

today = datetime.date.today()
age = relativedelta.relativedelta(today, dob)

print person['name'] +"\'s age today is:"
print str(age.years).rjust(2) + " years"
print str(age.months).rjust(2) + " months"
print str(age.days).rjust(2) + " days"

if (age.months == age.days == 0):
	cake = u'\U0001F382'.encode('utf-8')
	cakeline = ' '.join([cake for i in xrange(14)])
	border_cakes = ' '.join([cake for i in xrange(2)])

	print '\n', cakeline	
	print border_cakes, '   Happy Birthday! ', border_cakes
	print cakeline
