<%@ page session="true" %>
<!DOCTYPE html>
<html>
<head>
    <title>Caretaker Dashboard</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

<h2>Welcome Caretaker: ${sessionScope.userName}</h2>

<a href="chat.jsp">💬 Chat with Elder</a><br>
<a href="reports.jsp">📈 Reports</a><br>
<a href="LogoutServlet">Logout</a>

<h3>Assigned Elders</h3>
<!-- Data will be loaded using servlet -->

</body>
</html>
