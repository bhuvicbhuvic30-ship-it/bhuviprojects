package com.elder.servlet;

import com.elder.db.DBConnection;
import javax.servlet.*;
import javax.servlet.http.*;
import java.io.*;
import java.sql.*;

public class CaretakerDashboardServlet extends HttpServlet {

    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        try {
            Connection con = DBConnection.getConnection();
            Statement st = con.createStatement();

            ResultSet rs = st.executeQuery(
                "SELECT * FROM help_requests WHERE status='PENDING'"
            );

            req.setAttribute("requests", rs);
            RequestDispatcher rd =
                req.getRequestDispatcher("caretakerDashboard.jsp");
            rd.forward(req, resp);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
