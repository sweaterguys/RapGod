#RapGod.py
from flask import Flask, render_template, request, jsonify
from python.generate import generator
from multiprocessing import Value
global epoch, loss, step
counter = Value('i',0)

app = Flask(__name__)


@app.route('/')
def init():
	return render_template("index.html")

@app.route('/generate/', methods=['GET'])
def generate():
	with counter.get_lock():
		counter.value += 1
	rap = generator()
	data = {'rap': rap}
	data = jsonify(data)
	return data
@app.route('/stats/', methods=['GET'])
def stats():
	try:
		count=counter.value
		data = {'epoch':str(epoch), 'generated':str(count), "loss":str(loss), 'step':str(step)}
	except:
		data = {'epoch':"na", 'generated':"na", "loss":"na", "step":"na"}
	data = jsonify(data)
	return data

@app.route('/publish/epoch/', methods=['POST'])
def epoch():
	args = str(request.values)
	global epoch
	epoch = args.split('"epoch": ')[1].split(",")[0]

	return "hi"

@app.route('/publish/step/', methods=['POST'])
def step():
	args = request.data
	global step, loss
	step = args.split("step: ")[1].split("/")[0]
	loss = args.split("- loss: ")[1]

	return "hi"

if __name__ == '__main__':
	app.run(host="localhost",port="5000")
