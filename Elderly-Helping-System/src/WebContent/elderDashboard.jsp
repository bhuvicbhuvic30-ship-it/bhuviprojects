<%@ page session="true" %>
<!DOCTYPE html>
<html>
<head>
    <title>Elder Dashboard</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="js/maps.js"></script>
</head>
<body>

<h2>Welcome Elder: ${sessionScope.userName}</h2>

<a href="emergency.jsp">🚨 Emergency Help</a><br>
<a href="chat.jsp">💬 Chat with Caretaker</a><br>
<a href="reports.jsp">📊 View Reports</a><br>
<a href="LogoutServlet">Logout</a>

<h3>📍 Live Location</h3>
<div id="map" style="height:400px;"></div>

<script async
src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap">
</script>

</body>
</html>
