var port = "80"
var host = "35.196.198.150"
var ctx = document.getElementById("chart").getContext("2d");
var chart = new Chart(ctx, {
	type: 'line',
	data: {
		datasets: [{
			label: 'loss',
			borderColor: [
			'white'
			],
			borderWidth: 1
		}]
	},
	options: {

		legend: {
			display: false
		},
		scales: {
			yAxes: [{
				ticks: {
					display: false
				},
				gridLines: {
					display: false,
					drawBorder: false,
				}
			}],
			xAxes: [{
				ticks: {
					display: false
				},
				gridLines: {
					display: false,
					drawBorder: false,
				}
			}]
		}
	}
});

setInterval(function(){
	$.ajax({
		url: 'http://127.0.0.1:5000/stats/',
		method: 'GET',
		success: function(data) {
			$('#epoch').html('You are running Epoch Number: ' + data['epoch'])
			$('#generated').html(data['generated'] + " raps have been generated on RapGod.io")
			$('#loss').html("Current Loss (approaching 0): " + data['loss'])
			$('#step').html("Current Step Number: " + data['step'])
			$('#stream').html(data["stream"])
			chart.config.data.labels.push(1)
			chart.config.data.datasets[0].data.push(data['loss'])
			chart.update()
		}
	});
}, 500);
$( "#generate" ).click(function() {
	var MyMsg = {};
	$( "#page1" ).fadeOut(500, function() {
		$.ajax({
			url: 'http://'+host+':'+port+'/generate/',
			method: 'GET',
			success: function(data) {
				$( "#page3" ).fadeIn(500);
				$('#your_Rap').html(data['rap']);
				$('#YourRap').html("Your Rap");
				MyMsg.msg = new SpeechSynthesisUtterance(data['rap']);
				window.speechSynthesis.speak(MyMsg.msg);
			}
		});
		var elem = document.getElementById("myBar"); 
		var width = 10;
		var id = setInterval(frame, 30);
		function frame() {
			if (width >= 100) {
				clearInterval(id);
				$( "#loading" ).fadeOut(200, function() {
					$( "#rap" ).fadeIn(200);
				});
			} else {
				width++; 
				elem.style.width = width + '%'; 
				elem.innerHTML = width * 1 + '%';
			}
		}
	});
	return false;
});
$( "#re-generate" ).click(function() {
	var MyMsg = {};
	$( "#rap" ).fadeOut(200, function() {
		$.ajax({
			url: 'http://'+host+':'+port+'/generate/',
			method: 'GET',
			success: function(data) {
				$('#your_Rap').html(data['rap'])
				$('#YourRap').html("Your Rap")
				MyMsg.msg = new SpeechSynthesisUtterance(data['rap']);
				window.speechSynthesis.speak(MyMsg.msg);
			}
		});
		$( "#loading" ).fadeIn(100);
		var elem = document.getElementById("myBar"); 
		var width = 10;
		var id = setInterval(frame, 10);
		function frame() {
			if (width >= 100) {
				clearInterval(id);
				$( "#loading" ).fadeOut(200, function() {
					$( "#rap" ).fadeIn(200);
				});
			} else {
				width++; 
				elem.style.width = width + '%'; 
				elem.innerHTML = width * 1 + '%';
			}
		}
	});
	return false;
});
