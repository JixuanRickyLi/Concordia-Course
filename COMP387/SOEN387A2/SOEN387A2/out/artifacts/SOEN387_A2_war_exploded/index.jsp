<%@ page import="com.jixuanli.soen387.repository.core.*" %>
<%@ page import="java.sql.ResultSet" %><%--
  Created by IntelliJ IDEA.
  User: jixuanli
  Date: 10/28/19
  Time: 21:11
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
  <head>
    <title>$Title$</title>
  </head>
  <body>
  <table border="1" cellspacing="0" cellpadding="0">
      <tr>
          <th>id</th>
          <th>title</th>
          <th>description</th>
          <th>isbn</th>
          <th>publisher</th>
          <th>cover</th>
          <th>author</th>
      </tr>
<%
 Core myCore = new Core();
 Book[] rs = myCore.list_all_books();
 int i = rs.length;
 int c = 0;
 while(c < i){
     %>
      <tr>
          <%
              out.println("<td>"+
                      rs[c].getiD()+"</td><td>"+
                      rs[c].getTitle()+"</td><td>"+
                      rs[c].getDescription()+"</td><td>"+
                      rs[c].getiSBN()+"</td><td>"+
                      rs[c].getPublisher()+"</td><td>"+
                      rs[c].getCover()+"</td><td>"+
                      rs[c].getAuthor()+"</td>"
              );
              c++;
          %>
      </tr>
<%

 }

%>


  <%
      Book theBook = myCore.get_book(1);
  %>
      <tr>
          <%
              out.println("<td>"+
                      theBook.getiD()+"</td><td>"+
                      theBook.getTitle()+"</td><td>"+
                      theBook.getDescription()+"</td><td>"+
                      theBook.getiSBN()+"</td><td>"+
                      theBook.getPublisher()+"</td><td>"+
                      theBook.getCover()+"</td><td>"+
                      theBook.getAuthor()+"</td>"
              );
          %>
      </tr>
      <%
    %>

  </table>
  </body>
</html>
