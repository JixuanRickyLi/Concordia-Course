package Servlet;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Enumeration;

/**
 * @author: Jingchao Zhang
 * @createDate: 2019/09/28
 **/

@WebServlet("/display")
public class DisplayHttpRequest extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        handleRequest(request, response);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        handleRequest(request, response);
    }

    protected void handleRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String method = request.getMethod();
        String format = request.getParameter("format");
        Enumeration<String> headerNames = request.getHeaderNames();
        Enumeration<String> parameterNames = request.getParameterNames();
        PrintWriter out = response.getWriter();
        if (format == null || format.equals("html")) {
            response.setContentType("text/html");
            out.println("<!DOCTYPE html>\n" +
                    "<html lang=\"en\">\n" +
                    "<head>\n" +
                    "<meta charset=\"UTF-8\">\n" +
                    "<title>Basic Servlet</title>\n" +
                    "<style>\n" +
                    "table, th, td {\n" +
                    "border: 1px solid black; border-collapse: collapse; padding: 5px; text-align:left;}\n" +
                    "</style>\n" +
                    "</head>\n" +
                    "<body>\n");

            out.println("");

            // Request Method Table
            out.println("<table style=\"width:50%;\">\n" +
                    "<tr>\n" +
                    "<th style=\"width:25%;\">Request Method: </th>\n" +
                    "<td>" + method + "</td>\n" +
                    "</tr>\n" +
                    "</table>\n");
            out.println("</br>");

            // Request Headers Table
            out.println("<table style=\"width:50%;\">\n" +
                    "<tr><th colspan=\"2\">Request Headers: </th></tr>\n");
            while (headerNames.hasMoreElements()) {
                String key = headerNames.nextElement();
                String value = request.getHeader(key);

                key = StringUtils.encodeHtml(key);
                value = StringUtils.encodeHtml(value);

                out.println("<tr>" +
                        "<th>" + key +"</th>" +
                        "<td>" + value + "</td>" +
                        "</tr>");
            }
            out.println("</table>");
            out.println("</br>");

            // Request Parameters Table
            out.println("<table style=\"width:50%;\">\n" +
                    "<tr><th colspan=\"2\">Query String: </th></tr>");
            while (parameterNames.hasMoreElements()) {
                String key = parameterNames.nextElement();
                String value = request.getParameter(key);

                key = StringUtils.encodeHtml(key);
                value = StringUtils.encodeHtml(value);

                out.println("<tr>" +
                        "<th>" + key +"</th>" +
                        "<td>" + value + "</td>" +
                        "</tr>");
            }
            out.println("</table>\n");
            out.println("</body>\n" +
                    "</html>");
        } else if (format.equals("text")) {
            response.setContentType("text/plain");
            out.println("Request Method:  " + method + "\n");
            out.println("Request Headers:");
            while (headerNames.hasMoreElements()) {
                String key = headerNames.nextElement();
                out.println("\t" + key + ": " + request.getHeader(key));
            }
            out.println("\nQuery String:");
            while (parameterNames.hasMoreElements()) {
                String key = parameterNames.nextElement();
                out.println("\t" + key + ": " + request.getParameter(key));
            }
        } else if (format.equals("xml")) {
            response.setContentType("text/xml;charset=UTF-8");
            out.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
            out.append("<response><request-method>").append(method).append("</request-method>");
            out.append("<request-headers>");
            while (headerNames.hasMoreElements()){
                String key = headerNames.nextElement();
                String value = request.getHeader(key);

                key = StringUtils.encodeHtml(key);
                value = StringUtils.encodeHtml(value);

                out.append("<header name=\"").append(key).append("\">").append(value).append("</header>");
            }
            out.append("</request-headers>");
            out.append("<query-string>");
            while (parameterNames.hasMoreElements()){
                String key = parameterNames.nextElement();
                String value = request.getParameter(key);

                key = StringUtils.encodeHtml(key);
                value = StringUtils.encodeHtml(value);

                out.append("<").append(key).append(">").append(value).append("</").append(key).append(">");
            }
            out.append("</query-string>");
            out.append("</response>");
            out.println();
        } else {
            throw new ServletException("The server cannot parse this format: " + format);
        }

        out.flush();
    }
}