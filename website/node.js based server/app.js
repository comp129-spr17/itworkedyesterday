var express = require('express');
var todoController = require('./controllers/todoController');
var port = 80;
var app = express();

//set up template engine
app.set('view engine', 'ejs');

//static files
app.use(express.static('./public'));

//fire controllers
todoController(app);

//listen to port
app.listen(port);
console.log('You are listening to port ', port);
