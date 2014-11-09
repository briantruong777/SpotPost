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

	$.getJSON('http://localhost:5000/spotpost/_get', {username: "Admin", min_rating: "11", max_rating: "40"}, function(data){
		var baseHTML = "<tr><th>ID</th><th>Content</th><th>Rating</th><th>Longitude</th><th>Latitude</th><th>Username</th><th>Time</th></tr>"
		for(var i = 0; i < data.length; i++){
			baseHTML += "<tr><td>" + data[i].id + "</td><td>" + data[i].content + "</td><td>" + data[i].rating 
						+ "</td><td>" + data[i].longitude + "</td><td>" + data[i].latitude + "</td><td>" + data[i].username + "</td><td>" + data[i].time + "</td></tr>";
			$("#testing").html(baseHTML);
		}
	});
});