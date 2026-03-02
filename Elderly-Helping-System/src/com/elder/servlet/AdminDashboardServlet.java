package com.elder.servlet;

import com.elder.db.DBConnection;
import javax.servlet.*;
import javax.servlet.http.*;
import java.io.*;
import java.sql.*;

public class AdminDashboardServlet extends HttpServlet {

    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        try {
            Connection con = DBConnection.getConnection();
            Statement st = con.createStatement();

            ResultSet users = st.executeQuery("SELECT * FROM users");
            req.setAttribute("users", users);

            RequestDispatcher rd =
                req.getRequestDispatcher("adminDashboard.jsp");
            rd.forward(req, resp);

        } catch(Exception e){
            e.printStackTrace();
        }
    }
}
