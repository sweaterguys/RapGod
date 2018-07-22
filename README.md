
![license](https://img.shields.io/github/license/mashape/apistatus.svg)
![Docker Build Status](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg)
![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

# RapGod.io
**[rapgod.io](rapgod.io)**

Rap God uses an LSTM to generate word strings that make some sense and get better with time.
It trains (train.py) on `raps.txt` (a database of 15k bars from our favourite rappers).
It generates original bars using another neural network to interpret the data.

The [website](rapgod.io) is hosted on GCloud as a Flask compute engine running on an 8-core CPU high memory computer.
Flask allows `push` and `pull` requests to easily render templates with Python, in a sense allowing you to modify HTML dynamically with JavaScript using parameters from Python's output. 

When a user opens the website, a `get` request to Flask renders the HTML, JavaScript, and CSS statically. Every 500 milliseconds, a `get` request from JavaScript on the website grabs the most recent training data to update the graph and the top right monitor. 

When the user hits **generate** a `get` method is sent to Flask which triggers `generate.py` to return a verse of rap. 
This means that every single rap will be unique and original; no two users will ever hear the same rap.

## Usage

- Install Python 2.7

- Install PIP

- Install requirements:

`pip install -r requirements.txt`

For local hosting:

- Change ports on the following files: 
	- app.py (`localhost:5000`)
	- static/scripts/script.js (`127.0.0.1:5000`)
	- train.py (`127.0.0.1:5000`)

For web hosting: 

- Change ports on the following files: 
	- app.py (`0.0.0.0:80`)
	- static/scripts/script.js (`YOUR_EXTERNAL_IP:80`)
	- train.py (`YOUR_EXTERNAL_IP:80`)


- Run `./run.sh`

## Docker

Build the container:

`docker build . -t rapgod`

Run the container in interactive mode:

`docker run --name=rapgod -p 80:80 -it rapgod:latest /bin/bash`

And then run with `./run.sh`

## Next Steps:
- [ ] Make Generate lighter

- [ ] Fix JS bugs

- [ ] Run train and app seperately with a shared bucket for training data

- [ ] Mobile Support

- [ ] Integrate with Lyrebird to generate a unique RapGod voice

## Credits: 
- Ted Spare (Algorithm, generate.py, train.py)
- Dexter Storey (Flask, HTML, CSS, JS)
- Jonah Dutz (general ML research and help on train.py, generate.py)
- Caleb Hoyne (Python, JS, hackathon OG)
- Michel Can (AWS and GCloud Deployment)
- Dom Defelice (Python, moral support)

- _Special thanks to StackOverflow and Medium._
