package com.elder.servlet;

import com.elder.db.DBConnection;
import com.elder.util.PasswordUtil;
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.sql.*;

public class RegisterServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        try {
            Connection con = DBConnection.getConnection();

            String hashed = PasswordUtil.hashPassword(req.getParameter("password"));

            PreparedStatement ps = con.prepareStatement(
                "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)"
            );

            ps.setString(1, req.getParameter("name"));
            ps.setString(2, req.getParameter("email"));
            ps.setString(3, hashed);
            ps.setString(4, req.getParameter("role"));

            ps.executeUpdate();
            resp.sendRedirect("login.jsp");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
