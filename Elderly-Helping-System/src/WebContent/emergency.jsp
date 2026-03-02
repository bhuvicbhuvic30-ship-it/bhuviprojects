<%@ page session="true" %>
<!DOCTYPE html>
<html>
<head>
    <title>Emergency</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

<h2>🚨 Emergency Help</h2>

<form action="EmergencyServlet" method="post">
    <textarea name="message" placeholder="Describe emergency..." required></textarea><br>
    <input type="submit" value="Send Alert">
</form>

<a href="elderDashboard.jsp">Back</a>

</body>
</html>
