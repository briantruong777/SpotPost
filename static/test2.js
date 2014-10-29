var button = document.getElementById("testButton");
button.addEventListener("click", function(){
	/*
	var paragraph = document.getElementById("para");
	paragraph.innerHTML = "Nothing so far."

	var send_data = {content: "JSON Test, Here's hoping it works!", photo_id: 7, user_id: 4, longitude: "80E", latitude: "10N", visibility: 10, rating: 18};
	$.post('http://localhost:5000/post', send_data, function(){
		paragraph.innerHTML = "Hurray it works!"
	});
	*/

	$.getJSON('http://localhost:5000/get', {num: "", morenum: "5", user: ""}, function(data){
		var baseHTML = "<tr><th>Num</th><th>Text</th><th>Morenum</th><th>User</th></tr>"
		for(var i = 0; i < data.length; i++){
			baseHTML += "<tr><td>" + data[i].num + "</td><td>" + data[i].words + "</td><td>" + data[i].morenum 
						+ "</td><td>" + data[i].user + "</td></tr>";
			$("#testing").html(baseHTML);
		}
	});
});