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

// 404
app.get('*', function(req, res){
  //res.redirect('/');
  res.status(404).send('404');
});

function intermittent() {
	var spawn = require("child_process").spawn;
	var process = spawn('python',["../python/intermittent.py"])
	console.log('ran a intermittent python script')
}
setInterval(intermittent, 5000);

app.listen(9190, function() {
	var spawn = require("child_process").spawn;
	var process = spawn('python',["../python/persistent.py"])
	console.log('started persistent')
});
module.exports = app