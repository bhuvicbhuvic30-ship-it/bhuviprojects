<h2>Submit Complaint</h2>

<form action="ComplaintServlet" method="post">

Student Email<br>
<input type="text" name="email"><br>

Category<br>
<select name="category">

<option>Academic</option>
<option>Infrastructure</option>
<option>Hostel</option>
<option>WiFi</option>
<option>Sanitation</option>

</select>

<br><br>

Description<br>
<textarea name="description"></textarea>

<br><br>

<input type="submit" value="Submit Complaint">

</form>
