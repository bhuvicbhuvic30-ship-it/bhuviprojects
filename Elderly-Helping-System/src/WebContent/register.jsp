<%@ page language="java" contentType="text/html; charset=UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

<h2>User Registration</h2>

<form action="RegisterServlet" method="post">
    Name: <input type="text" name="name" required><br>
    Email: <input type="email" name="email" required><br>
    Password: <input type="password" name="password" required><br>
    Role:
    <select name="role">
        <option value="ELDER">Elder</option>
        <option value="CARETAKER">Caretaker</option>
    </select><br>
    <input type="submit" value="Register">
</form>

</body>
</html>
