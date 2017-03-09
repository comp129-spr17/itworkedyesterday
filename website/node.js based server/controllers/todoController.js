var bodyParser = require('body-parser');

var data = [{item: 'get milk'}, {item: 'walk dog'},{item: 'test some code cause why not'}];
var dataC = [{item: 'buy stuff at store'}];
var urlencodedParser = bodyParser.urlencoded({extended: false});

module.exports = function(app){

//request handlers
app.get('/', function(req, res){
  res.render('todo', {todos: data});
});

app.get('/todo', function(req, res){
  res.render('todo', {todos: data});
});

app.get('/login', function(req, res){
  res.render('login', {todos: data});
});

app.get('/completed', function(req, res){
  res.render('completed', {todos: dataC});
});

app.delete('/completed/:item', function(req, res){
  dataC = dataC.filter(function(todo){
    return todo.item.replace(/ /g, '-') !== req.params.item;
  });
  res.json(dataC);
});

app.post('/completed', urlencodedParser, function(req, res){
  dataC.push(req.body);
  res.json(dataC);
});

app.post('/todo', urlencodedParser, function(req, res){
  data.push(req.body);
  res.json(data);
});

app.delete('/todo/:item', function(req, res){
  data = data.filter(function(todo){
    return todo.item.replace(/ /g, '-') !== req.params.item;
  });
  res.json(data);
});

};
