
![license](https://img.shields.io/github/license/mashape/apistatus.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/google/skia.svg)
![Docker Build Status](https://img.shields.io/docker/build/jrottenberg/ffmpeg.svg)
![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

# RapGod.io
[rapgod.io](rapgod.io)

Rap God uses an AI to generate word strings that in theory make sense and get better with time.
It trains (train.py) on raps.txt (a database of bars from our favourite rappers)
It generates original bars using another neural network to interpret the data.

The website (rapgod.io) is hosted on GCloud as a flask compute engine running on an 8 core CPU high memory computer
Flask allows push and pull requests to easily render templates with python, in a sense allowing you to modify html dynamicly with js using perameters from python output. 

When a user opens the website, a get request to flask renders the html, Js, and Css statically, every 500 milliseconds, a get request from js on the website grabs the most recent training data to update the graph and the top right monitor. 
When the user hits "generate" A get method is sent to flask which then triggers generate.py to return a verse of rap. 
This means that every single rap will be unique and original, no user will ever hear the same rap.

## Usage
- install python2.7

- install pip

run: `pip install -r requirements.txt`

	For local hosting:
	- change ports on the following files: 
		app.py (localhost:5000)
		static/scripts/script.js (127.0.0.1:5000)
		train.py (127.0.0.1:5000)

	For web hosting: 
	- change ports on the following files: 
		app.py (0.0.0.0:80)
		static/scripts/script.js (YOUR_EXTERNAL_IP:80)
		train.py (YOUR_EXTERNAL_IP:80)


run `./run.sh`

## Docker

Build the container:
```
docker build . -t rapgod 
```

Run the container in interactive mode:
```
docker run --name=rapgod -p 80:80 -it rapgod:latest /bin/bash
```
And then run `./run.sh`

## Next Steps:
- Make Generate lighter

- Fix JS bugs

- Run train and app seperately with a shared bucket for training data

- Mobile Support

- Integrate with Lyrebird

## Credits: 
- Ted Spare (AI algorithm, Generate.py, Train.py)
- Dexter Storey (Flask, HTML, CSS, JS)
- Jonah Dutz (general ML research and help on Train.py, Generate.py)
- Caleb Hoyne (python, js - OG HACKATHON)
- Michael Can (AWS and GCLOUD Deployment)
- Dom Defelice (Python + Moral Support)

- Stack Overflow, Medium Cheers guys.
