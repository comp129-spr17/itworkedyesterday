
function addTask() {
	var task = document.getElementById("titleInput").value
	var text = document.createTextNode(task)
	var newTask = document.createElement("li")

	newTask.appendChild(text)
	document.getElementById("todoList").appendChild(newTask)
}