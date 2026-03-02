package com.elder.servlet;

import com.elder.db.DBConnection;
import javax.servlet.*;
import javax.servlet.http.*;
import java.io.*;
import java.sql.*;

public class HelpRequestServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        try {
            HttpSession session = req.getSession();
            int elderId = (int) session.getAttribute("userId");

            Connection con = DBConnection.getConnection();

            PreparedStatement ps = con.prepareStatement(
                "INSERT INTO help_requests(elder_id,description,status) VALUES(?,?,?)"
            );

            ps.setInt(1, elderId);
            ps.setString(2, req.getParameter("description"));
            ps.setString(3, "PENDING");

            ps.executeUpdate();
            resp.sendRedirect("elderDashboard.jsp");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
