from flask import Flask, request, render_template
from dashboard import get_values
from time import localtime, strftime, time, sleep

app = Flask(__name__)

a = 1

@app.route('/home')
def index():
	global a
	print("Url request " + str(a))
	a += 1

	# get time and current day of month for stats calcultation
	datetime = strftime("%d.%m.%Y", localtime())

	day = str(datetime[:2])
	current_time = time()
	datetime = [day, datetime]

	# return a dict with the stats {user_id:[name, current_month_won, target, current_day_won]
	values = get_values(current_time, day)

	if values == False:
		return "API request failed"
		
	x, y, z = 0, 0, 0

	for entry in values:
		# summing the teams total current_month_won
		x += values[entry][1]
		# summing the teams total target
		y += values[entry][2]
		# summing the teams total current_day_won
		z += values[entry][3]

	total = [x, y, z]

	# create sorted list from dict; sorted by second value (name)
	values = sorted(values.items(), key = lambda t: t[1])

	datetime[0] = int(datetime[0])

	return render_template('index.html', values = values, total = total, datetime = datetime)

if __name__=='__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)