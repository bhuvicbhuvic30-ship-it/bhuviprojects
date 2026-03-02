package com.elder.servlet;

import com.elder.db.DBConnection;
import javax.servlet.*;
import javax.servlet.http.*;
import java.io.*;
import java.sql.*;

public class EmergencyServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        try {
            HttpSession session = req.getSession();
            int elderId = (int) session.getAttribute("userId");

            Connection con = DBConnection.getConnection();

            PreparedStatement ps = con.prepareStatement(
                "INSERT INTO emergency_alerts(elder_id,message,latitude,longitude) VALUES(?,?,?,?)"
            );

            ps.setInt(1, elderId);
            ps.setString(2, req.getParameter("message"));
            ps.setDouble(3, Double.parseDouble(req.getParameter("lat")));
            ps.setDouble(4, Double.parseDouble(req.getParameter("lng")));

            ps.executeUpdate();
            resp.getWriter().println("Emergency Sent!");

        } catch(Exception e){
            e.printStackTrace();
        }
    }
}
