package servlet;

import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.sql.*;
import db.DBConnection;

public class ComplaintServlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String email = request.getParameter("email");
        String category = request.getParameter("category");
        String description = request.getParameter("description");

        try {

            Connection con = DBConnection.getConnection();

            PreparedStatement ps = con.prepareStatement(
                    "insert into complaints(student_email,category,description) values(?,?,?)");

            ps.setString(1, email);
            ps.setString(2, category);
            ps.setString(3, description);

            ps.executeUpdate();

            response.getWriter().println("Complaint Submitted Successfully!");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
