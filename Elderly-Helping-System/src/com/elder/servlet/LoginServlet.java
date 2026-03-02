package com.elder.servlet;

import com.elder.db.DBConnection;
import com.elder.util.PasswordUtil;
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.sql.*;

public class LoginServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        try {
            Connection con = DBConnection.getConnection();

            String hashed = PasswordUtil.hashPassword(req.getParameter("password"));

            PreparedStatement ps = con.prepareStatement(
                "SELECT * FROM users WHERE email=? AND password=?"
            );

            ps.setString(1, req.getParameter("email"));
            ps.setString(2, hashed);

            ResultSet rs = ps.executeQuery();

            if (rs.next()) {

                HttpSession session = req.getSession();
                session.setAttribute("userId", rs.getInt("id"));
                session.setAttribute("role", rs.getString("role"));
                session.setAttribute("name", rs.getString("name"));

                String role = rs.getString("role");

                if (role.equals("ELDER"))
                    resp.sendRedirect("elderDashboard.jsp");
                else if (role.equals("CARETAKER"))
                    resp.sendRedirect("caretakerDashboard");
                else
                    resp.sendRedirect("adminDashboard");

            } else {
                resp.getWriter().println("Invalid Credentials");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
