import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpContext;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.*;
import java.net.InetSocketAddress;
import java.net.URI;
import java.nio.charset.StandardCharsets;

/**
 * @author: Jingchao Zhang
 * @createDate: 2019/09/29
 **/
public class SimpleHttpServer {
    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        HttpContext context = server.createContext("/");
        context.setHandler(SimpleHttpServer::handleRequest);
        server.start();
    }

    private static void handleRequest(HttpExchange exchange) throws IOException {
        Headers responseHeaders = exchange.getResponseHeaders();
        URI requestURI = exchange.getRequestURI();
        if (requestURI.toString().startsWith("/css")) {
            responseHeaders.set("Content-Type", "text/css");
        } else {
            responseHeaders.set("Content-Type", "text/html");
        }
        File file;
        if (requestURI.toString().equals("/")) {
            file = new File ("web/index.html").getCanonicalFile();
        } else {
            file = new File ("web" + requestURI).getCanonicalFile();
        }
        if (!file.isFile()) {
            String notFound = "<h1>404 Not Found</h1>";
            exchange.sendResponseHeaders(404, notFound.length());
            OutputStream out = exchange.getResponseBody();
            out.write(notFound.getBytes(StandardCharsets.UTF_8));
            out.close();
            return;
        }
        byte[] byteArray  = new byte [(int)file.length()];
        try (FileInputStream fis = new FileInputStream(file);
             BufferedInputStream bis = new BufferedInputStream(fis)
        ){
            bis.read(byteArray, 0, byteArray.length);
            exchange.sendResponseHeaders(200, file.length());
            OutputStream outputStream = exchange.getResponseBody();
            outputStream.write(byteArray,0, byteArray.length);
            outputStream.close();
        }
    }
}
