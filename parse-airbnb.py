# encoding=utf8
import argparse, sys

reload(sys)
sys.setdefaultencoding('utf8')

import csv, json
from datetime import datetime, timedelta, date

# load from arguments

parser=argparse.ArgumentParser()

parser.add_argument('--aggregation', '-a', help="Aggregate by week or month", type=str, default = "month")
parser.add_argument('--input', '-i', help="Name of the input file", type=str, default = "input/calendar.csv")
parser.add_argument('--output', '-o', help="Name of the output file", type= str, default= 'output/aggregated_calendar.csv')

args=parser.parse_args()

results = {}

lines = 0

with open(args.input) as csv_file:
	lines = sum(1 for line in csv_file)

with open(args.input) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0

	headers = next(csv_reader, None)  # skip the headers

	count = 0

	for row in csv_reader:
		# datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
		datetime_object = datetime.strptime(row[1], '%Y-%m-%d')

		key = ''

		count = count + 1;
		if count % 1000 == 0:
			print count
		# if count == 100000:
		# 	break

		if args.aggregation == 'week':
			key = datetime_object.strftime("%Y-%V")
		elif args.aggregation == 'month':
			key = datetime_object.strftime("%Y-%m")

		id = row[0]
		try:
			price = float(row[4].replace("$","").replace(",",""))
			if id not in results:
				results[id] = {}
				# print 'created', id

			if key not in results[id]:
				results[id][key] = []
				# print 'created', key, 'for', id
			results[id][key].append(price)
		except:
			print 'impossible to parse', row[4]

	#
	# # now that the csv has been parsed, aggregate
	# print json.dumps(results)
	with open(args.output, mode='w') as out_file:
		csv_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow(['ID', 'Date', 'Average price'])

		for id in results:
			for key in results[id]:
				average = sum(results[id][key], 0.0) / len(results[id][key])
				csv_writer.writerow([id, key, average])
