var spawn = require("child_process").spawn;

var process = spawn("python", ["rapgod.py"]);

process.stdout.on("data", function(data) {
	res.send(data.toString());
})
