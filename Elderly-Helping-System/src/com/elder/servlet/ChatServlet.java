package com.elder.servlet;

import com.elder.db.DBConnection;
import javax.servlet.*;
import javax.servlet.http.*;
import java.io.*;
import java.sql.*;

public class ChatServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        try {
            Connection con = DBConnection.getConnection();

            PreparedStatement ps = con.prepareStatement(
                "INSERT INTO chat_messages(sender_id,receiver_id,message) VALUES(?,?,?)"
            );

            ps.setInt(1, Integer.parseInt(req.getParameter("sender")));
            ps.setInt(2, Integer.parseInt(req.getParameter("receiver")));
            ps.setString(3, req.getParameter("message"));

            ps.executeUpdate();
            resp.getWriter().println("Message Sent");

        } catch(Exception e){
            e.printStackTrace();
        }
    }
}
