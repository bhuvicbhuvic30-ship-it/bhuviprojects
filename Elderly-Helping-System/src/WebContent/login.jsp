<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<h2>Elderly Helping System - Login</h2>

<form action="LoginServlet" method="post">
    Email: <input type="email" name="email" required><br>
    Password: <input type="password" name="password" required><br>
    Role:
    <select name="role">
        <option value="ELDER">Elder</option>
        <option value="CARETAKER">Caretaker</option>
        <option value="ADMIN">Admin</option>
    </select><br>
    <input type="submit" value="Login">
</form>

<p>New user? <a href="register.jsp">Register here</a></p>

<p style="color:red;">
    <%= request.getAttribute("error") != null ? request.getAttribute("error") : "" %>
</p>

</body>
</html>
