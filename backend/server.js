// Express startup
var http = require('http')
var express = require('express')
var bodyParser = require('body-parser')
var fs = require('fs')
var util = require('util');
var request = require('request')
var requirejs = require('requirejs')

var app = express()

var logFile = fs.createWriteStream('requests.log', { flags: 'a' });
var logStdout = process.stdout;
var tick = 0
var locationdata
var stream = 0
var spawnNATS = require("child_process").spawn;
var processNATS = spawnNATS('python',["../main.py", stream])


app.use(bodyParser.json({extended: true}))
app.use('/', express.static('../frontend'))

requirejs([], function (ubilabs) {
    console.log("server opened on port 9190")
	console.log("requests log file at ./requests.log")
})

// Enable CORS
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*")
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
    next()
})

// Receive data from client by invoking GET /python
app.get('/python', function(req,res){
    console.log('received a request from client ' + req.ip)
	logFile.write('hit');
	
	//Python test
	var spawn = require("child_process").spawn;
	var process = spawn('python',["../python/active.py"])
	
	//Get printout from python script into data
	process.stdout.on('data', function(data) { 
        res.send(data.toString()); 
    } )
	
})

app.get('/update', function(req, res){
    console.log("got a GET ping from the client");
    //return res.status(200).json(JSON.parse(locationdata));
	//console.log(locationdata)
	return res.status(200).json(locationdata);
});

app.post('/form', function(req, res){
    console.log("Received a stream change request from the client:");
	//console.log(req.body.stream);
	stream = req.body.stream
	loadNATS()
	
	res.status(200).json(JSON.stringify({'data': 'Data stream changed!'}))
});

app.post('/data', function(req, res){
    console.log('received location data');
	//console.log(req);
    //console.log(JSON.stringify(req.body));
	//logFile.write(req);
	locationdata = req.body
	res.send('')
});

// 404
app.get('*', function(req, res){
  //res.redirect('/');
  res.status(404).send('404');
});

function intermittent() {
	tick = tick + 1
	var spawn = require("child_process").spawn;
	var process = spawn('python', ["../python/intermittent.py", tick])
	
	process.stdout.on('data', function(data){
		console.log('ran an intermittent python script, got: ')
		console.log(data.toString())
		locationdata = data.toString()
	})

}
//setInterval(intermittent, 1000);

function loadNATS() {
	processNATS.kill()
	spawnNATS = require("child_process").spawn;
	processNATS = spawnNATS('python',["../main.py", stream])
	console.log('begin NATS data collection')
}
setInterval(loadNATS, 10000);

app.listen(9190, function() {
	loadNATS()
});
module.exports = app