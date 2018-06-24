URL = "http://127.0.0.1:5000";

var ctx = document.getElementById("chart").getContext("2d");
var chart = new Chart(ctx, {
	type: 'line',
	data: {datasets: [{label: 'loss',borderColor: ['white'],borderWidth: 1}]},
	options: {legend: {display: false},scales: {
	yAxes: [{ticks: {display: false},gridLines: {display: false,drawBorder: false,}}],
	xAxes: [{ticks: {display: false},gridLines: {display: false,drawBorder: false,}}]
	}}});

setInterval(function(){
	$.ajax({
		url: URL+"/stats/",
		method: 'GET',
		success: function(data) {
			$('#epoch').html('You are running Epoch Number: ' + data.epoch);
			$('#generated').html(data.generated + " raps have been generated on RapGod.io");
			$('#loss').html("Current Loss (approaching 0): " + data.loss);
			$('#step').html("Current Step Number: " + data.step);
			$('#stream').html(data.stream);
			chart.config.data.labels.push(1);
			chart.config.data.datasets[0].data.push(data.loss);
			chart.update();
		}
	});
}, 1000);

function load() {
	$("#loading").fadeIn(200);
	var elem = document.getElementById("myBar"); 
	var width = 10;
	var id = setInterval(frame, 30);
	function frame() {
		if (width >= 100) {
			clearInterval(id);
		} else {
			width++; 
			elem.style.width = width + '%'; 
			elem.innerHTML = width * 1 + '%';
		}
	}
}

function generate() {
	var MyMsg = {};
	$.ajax({
		url: URL+"/generate/",
		method: 'GET',
		success: function(rap) {
			$('#your_Rap').html(rap);
			$('#YourRap').html("Your Rap");
			$("#loading").fadeOut(200, function() {
				$("#rap").fadeIn(200);
				MyMsg.msg = new SpeechSynthesisUtterance(rap);
				window.speechSynthesis.speak(MyMsg.msg);
			});
		}
	});
}

$("#generate").click(function() {
	$("#page1").fadeOut(500, function() {
		$("#page3").fadeIn(500);
		load();
		generate();
	});
	return false;
});

$("#re-generate").click(function() {
	$("#rap").fadeOut(200);
	load();
	generate();
	return false;
});
