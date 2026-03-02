<%@ page session="true" %>
<!DOCTYPE html>
<html>
<head>
    <title>Chat</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

<h2>💬 Chat</h2>

<div id="chatBox" style="height:300px; overflow:auto; border:1px solid black;">
</div>

<form action="ChatServlet" method="post">
    <input type="text" name="message" required>
    <input type="submit" value="Send">
</form>

<a href="LogoutServlet">Logout</a>

</body>
</html>
