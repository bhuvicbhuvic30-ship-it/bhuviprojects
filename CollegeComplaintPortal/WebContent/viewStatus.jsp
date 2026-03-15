<%@ page import="java.sql.*" %>
<%@ page import="db.DBConnection" %>

<h2>Your Complaints</h2>

<%

Connection con = DBConnection.getConnection();

Statement st = con.createStatement();

ResultSet rs = st.executeQuery("select * from complaints");

while(rs.next()){

%>

Category: <%=rs.getString("category")%><br>
Description: <%=rs.getString("description")%><br>
Status: <%=rs.getString("status")%>

<hr>

<%

}

%>
