import packet.Packet;

import java.io.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.nio.channels.ClosedChannelException;
import java.nio.channels.DatagramChannel;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Set;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static java.nio.channels.SelectionKey.OP_READ;

public class Library {


    private String host;
    private int port;

    /* a3 adding variables for routing */
    private String serverHost = "http://localhost";
    private Integer serverPort = 3000;
    private String routerHost = "http://localhost";
    private Integer routerPort = 8007;
    private boolean handshake = false;
    private Long sequenceNumber;
    private static final Logger logger = LoggerFactory.getLogger(Library.class);

    /*use specific data structure to store required information*/
    private HashMap<String,String> header = new HashMap<>();
    private String body;
    private HashMap<String,String> query = new HashMap<>();

    public String send(String method, String str) throws MalformedURLException, IOException{

    	if(str.indexOf("http://")==-1) {
    			if(str.indexOf("txt")==-1) {
    				str="get -v 'http://localhost'";
    			}
    			else {
    				String fileName=str.substring(str.indexOf("/"));
    				str="get -v 'http://localhost"+fileName+"'";
    			}
    	}
    	
        /*to get host and port from given URL*/
        String url = str.substring(str.indexOf("http://"), str.indexOf("'",str.indexOf("http://")));
        URL u = new URL(url);
        serverHost = u.getHost();
        if(serverHost.equals("localhost")){
            serverPort = u.getPort() ;
        }
        else {
            port = 8007;
        }

//        port = 8080;
        if(str.contains("?")) {
            queryParameters(u);//handle query parameters
        }

//        String response = null;

//        try {

            /*commented out by Jixuan  , For A3, we need a new sending method*/
            /*open a socket*/
//            Socket socket = new Socket();
//            SocketAddress socketAddress = new InetSocketAddress(host, port);
//            socket.connect(socketAddress);


            /*send http request*/
//            generatePayload("GET",socket,str,u,url);
//
//            /*receive http response*/
//            response = receiveResponse("GET",socket,str,u,url);
//            if(response.contains("HTTP/1.0")||response.contains("HTTP/1.1")||response.contains("HTTP/2.0")){
//                if(needRedirection(response)){//check if this request needs to be redirected or not
//                    //ex:  httpc get 'http:httpbin.org/redirect-to?url=http://httpbin.org/get?course=networking&assignment=1&status_code=200'
//                    sendRequest(response,socket,str,u,query.get("url"));
//                    response = receiveResponse("POST",socket,str,u,query.get("url"));
//                }
//            }
//
//            /*close a socket*/
//            socket.close();
//        }catch (UnknownHostException e){
//            e.printStackTrace();
//        }catch (IOException e){
//            e.printStackTrace();
//        }
//        finally {
//            return response;
//        }

        //added by Jixuan Generate msg

//        generatePayload(method,
        String msg = "hi,s";
        //added by Jixuan, here we start a new connection
        SocketAddress routerAddress = new InetSocketAddress(routerHost, routerPort);
        InetSocketAddress serverAddress = new InetSocketAddress(serverHost, serverPort);
        String responsePayload = runClient(routerAddress, serverAddress, msg);
        String response = buildResponse(responsePayload,str);
        return response;
    }


   /*commented out by Jixuan merge POST and GET*/


//    public String POST(String str) throws MalformedURLException{
//
//    	if(str.indexOf("http://")==-1) {
//    		if(str.contains("post")){
//    			String fileName=str.substring(str.indexOf("/"));
//    			str="post -v -h Content-Type:application/json --d '{\"Assignment\": 210}' 'http://localhost"+fileName+"'";
//    		}
//    	}
//        /*to get host and port from given URL*/
//        String url = str.substring(str.indexOf("http://"), str.indexOf("'",str.indexOf("http://")));
//        URL u = new URL(url);
//        host = u.getHost();
//        if(host.equals("localhost")){
//            port = 8080;
//        }else {
//            port = u.getDefaultPort();
//        }
//        if(str.contains("?")) {
//            queryParameters(u);//handle query parameters
//        }
//
//        String response = null;
//
//        try {
//            /*open a socket*/
//            Socket socket = new Socket();
//            SocketAddress socketAddress = new InetSocketAddress(host, port);
//            socket.connect(socketAddress);
//
//            /*send http request*/
//            sendRequest("POST",socket,str,u,url);
//
//            /*receive http response*/
//            response = receiveResponse("POST",socket,str,u,url);
//            if(response.contains("HTTP/1.0")||response.contains("HTTP/1.1")||response.contains("HTTP/2.0")){
//                if(needRedirection(response)){//check if this request needs to be redirected or not
//                    //ex:  httpc post 'http:httpbin.org/redirect-to?url=http://httpbin.org/get?course=networking&assignment=1&status_code=200'
//                    sendRequest(response,socket,str,u,query.get("url"));
//                    response = receiveResponse("POST",socket,str,u,query.get("url"));
//                }
//            }
//
//            /*close a socket*/
//            socket.close();
//        }catch (UnknownHostException e){
//            e.printStackTrace();
//        }catch (IOException e){
//            e.printStackTrace();
//        }
//        finally {
//            return response;
//        }
//    }

    public void queryParameters(URL u){
        String queryLine = u.getQuery();
        String [] pair = queryLine.split("&");
        for (String s:pair) {
            String [] rest = s.split("=");
            query.put(rest[0],rest[1]);
        }
    }

    /*allow :get/post method ; str: whole command line input ; url: only the URL part*/
    public String generatePayload(String allow,Socket socket,String str,URL u,String url) throws IOException{

        /*default information setting(Notice : not all of http header field definitions are defined,only those that appeared in the assignment are defined)*/
        String connectionType = "close";
        String userAgent = "Chrome";
        String contentType = null;
        String contentLength = null;

        if(allow.equals("POST")) {//these options are only valid under POST request
            contentType = "text/plain";
            if(str.contains("-d")) {
                body = str.substring(str.indexOf("{", str.indexOf("-d")), str.indexOf("}") + 1);
            }else if(str.contains("-f")){
                String path = str.substring(str.indexOf("-f") + 3,str.indexOf(" ",str.indexOf("-f") + 3));
                body = readFile(path);
            }
            contentLength = String.valueOf(body.length());
        }

        /*initial headers to hash-map*/
        header.put("Host",this.host);
        header.put("Connection",connectionType);
        header.put("User-Agent",userAgent);
        if(allow.equals("POST")) {
            header.put("Content-Length", contentLength);
            header.put("Content-Type", contentType);
        }


        /*-h Header requirement:support multiple headers add or update*/
        String temp = str;
        String key;
        String value;
        for (int i = 0; i < str.length(); i++) {
            if(!temp.contains("-h")){
                break;
            }else{
                i = temp.indexOf("-h") + 3;
                temp = temp.substring(i);
                key = temp.substring(0,temp.indexOf(":",0));
                value = temp.substring(temp.indexOf(":",temp.indexOf(key))+ 1,temp.indexOf(" ",temp.indexOf(key)));
                if(header.containsKey(key)){
                    header.replace(key,value);
                    continue;
                }
                header.put(key,value);
            }
        }

        /*sending the request*/
        OutputStreamWriter outputStreamWriter = new OutputStreamWriter(socket.getOutputStream());
        BufferedWriter bufferedWriter= new BufferedWriter(outputStreamWriter);
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append(allow + " " + url + " HTTP/1.0\r\n");
        for (String keys:header.keySet()) {
            stringBuilder.append(keys).append(": ").append(header.get(keys)).append("\r\n");
        }
        if(allow.equals("POST")){
            stringBuilder.append("\r\n").append(body);
        }else if(allow.equals("GET")){
            stringBuilder.append("\r\n");
        }

        return stringBuilder.toString();
//        bufferedWriter.write(stringBuilder.toString());
//        bufferedWriter.flush();
    }

    /*str: whole command line input*/
    public String receiveResponse(String allow,Socket socket,String str,URL u,String url) throws IOException{
        InputStream inputStream = socket.getInputStream();
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
        StringBuilder stringBuilder = new StringBuilder();
        String data;
      
        do {
            data = bufferedReader.readLine();
            stringBuilder.append(data+"\r\n");
        }
        while (data != null);
        String response = stringBuilder.toString();
        bufferedReader.close();
        inputStream.close();

        /*verbose requirement*/
        if(str.contains("-v")) {//case that needs verbose
            if(needOutputFile(str)){//case need to output body data
                writeFile(response,str.substring(str.indexOf("-o") + 3));
            }
            return response;
        }else {//case that does not need verbose
            response = response.substring(response.indexOf("\r\n\r\n"));
            if(needOutputFile(str)){//case need to output body data
                writeFile(response,str.substring(str.indexOf("-o") + 3));
            }
        }
        return response;
    }

    public boolean needOutputFile(String str){
        if(str.contains("-o")){
            return true;
        }
        return false;
    }


    /*method to determine if the http response needs a redirection or not */
    public boolean needRedirection(String data){
        data = data.substring(0,20);//this is due to status will always be the first line, 0-20 characters for approximation of it.
        if(data.contains("300")||data.contains("301")||data.contains("302")||data.contains("304")){//satisfy any of those will need redirect
            return true;
        }
        return false;
    }
    public String readFile(String path) throws IOException {
        File file = new File(path);
        StringBuilder stringBuilder = new StringBuilder();
        BufferedReader bufferedReader = new BufferedReader(new FileReader(file));
        String nextLine;
        do {
            nextLine = bufferedReader.readLine();
            stringBuilder.append(nextLine);
        } while (nextLine != null);
        return stringBuilder.toString();
    }
    public void writeFile(String body, String filePath){
        File file = new File(filePath);
        BufferedWriter writer = null;
        try {
            writer = new BufferedWriter(new FileWriter(file));
            writer.write(body);
            writer.close();
        }catch (IOException e){
            e.printStackTrace();
        }
    }


    //For A3
    private String runClient(SocketAddress routerAddr, InetSocketAddress serverAddr, String message) throws IOException {

        DatagramChannel channel = DatagramChannel.open();
        channel.bind(serverAddr);

        /*handshake*/
        if(!handshake){
            sequenceNumber = this.handshake(channel, serverAddr, routerAddr);
        }

        /*transmit*/
        Packet p = null;
        if(message.getBytes().length <= Packet.MAX_LEN) {
            p = new Packet.Builder()
                    .setType(0)
                    .setSequenceNumber(++sequenceNumber)
                    .setPortNumber(serverAddr.getPort())
                    .setPeerAddress(serverAddr.getAddress())
                    .setPayload(message.getBytes())
                    .create();
        }else {
            return "data length is not allowed";
        }
       channel.send(p.toBuffer(), routerAddr);
        timer(channel,p,routerAddr);

        ByteBuffer buf = ByteBuffer.allocate(Packet.MAX_LEN);
        routerAddr = channel.receive(buf);
        buf.flip();
        Packet resp = Packet.fromBuffer(buf);
        if (resp.getType() == 1) {
            String payload = new String(resp.getPayload(), StandardCharsets.UTF_8);
            return payload;
        }

        return null;
    }



        /* example code */

//        try(DatagramChannel channel = DatagramChannel.open()){
//            String msg = "Hello World";
//            Packet p = new Packet.Builder()
//                    .setType(0)
//                    .setSequenceNumber(1L)
//                    .setPortNumber(serverAddr.getPort())
//                    .setPeerAddress(serverAddr.getAddress())
//                    .setPayload(msg.getBytes())
//                    .create();
//            channel.send(p.toBuffer(), routerAddr);
//
//            logger.info("Sending \"{}\" to router at {}", msg, routerAddr);
//
//            // Try to receive a packet within timeout.
//            channel.configureBlocking(false);
//            Selector selector = Selector.open();
//            channel.register(selector, OP_READ);
//            logger.info("Waiting for the response");
//            selector.select(5000);
//
//            Set<SelectionKey> keys = selector.selectedKeys();
//            if(keys.isEmpty()){
//                logger.error("No response after timeout");
//                return;
//            }
//
//            // We just want a single response.
//            ByteBuffer buf = ByteBuffer.allocate(Packet.MAX_LEN);
//            SocketAddress router = channel.receive(buf);
//            buf.flip();
//            Packet resp = Packet.fromBuffer(buf);
//            logger.info("Packet: {}", resp);
//            logger.info("Router: {}", router);
//            String payload = new String(resp.getPayload(), StandardCharsets.UTF_8);
//            logger.info("Payload: {}",  payload);
//
//            keys.clear();



    private long handshake(DatagramChannel channel,InetSocketAddress serverAddr, SocketAddress routerAddr) throws IOException{

        String msg = "HandShake Msg From Client";

        /*create package*/
        Packet p = new Packet.Builder()
                .setType(0)
                .setSequenceNumber(1)
                .setPortNumber(serverAddr.getPort())
                .setPeerAddress(serverAddr.getAddress())
                .setPayload(msg.getBytes())
                .create();

        /*send it to router*/
        channel.send(p.toBuffer(), routerAddr);

        logger.info("Sending handshake request \"{}\" to router at {}", msg, routerAddr);

        /*wait for response*/
        timer(channel, p,routerAddr);

        ByteBuffer byteBuffer = ByteBuffer.allocate(Packet.MAX_LEN);
        byteBuffer.clear();
        channel.receive(byteBuffer);
        byteBuffer.flip();
        Packet packet = Packet.fromBuffer(byteBuffer);

        logger.info("Message from server is :"+new String(packet.getPayload(), StandardCharsets.UTF_8));
        this.handshake = true;
        logger.info("Handshake done");
        System.out.println("Handshaked");
        return packet.getSequenceNumber();

    }

    int timerCounter = 0;
    private void timer(DatagramChannel channel, Packet packet, SocketAddress routerAddr ) throws IOException {

        channel.configureBlocking(false);
        Selector selector = Selector.open();
        channel.register(selector, OP_READ);
        selector.select(1000);

        Set<SelectionKey> keys = selector.selectedKeys();

        if (keys.isEmpty()) {
            logger.info("Handshake timed out {} times", ++timerCounter);

            channel.send(packet.toBuffer(), routerAddr);
            if(timerCounter < 10) {
                timer(channel, packet, routerAddr);
            }
            else{
                logger.error("timed out for {} times, stop trying", timerCounter);
                System.exit(100);
            }
        }
        keys.clear();
    }

    private String buildRequest(String allow, String str,String url) throws IOException{

        /*default information setting(Notice : not all of http header field definitions are defined,only those that appeared in the assignment are defined)*/
        String connectionType = "close";
        String userAgent = "COMP445";
        String contentType = null;
        String contentLength = null;
        if(allow.equals("POST")) {//these options are only valid under POST request
            contentType = "text/plain";
            if(str.contains("-d")) {
                body = str.substring(str.indexOf("{", str.indexOf("-d")), str.indexOf("}") + 1);
            }else if(str.contains("-f")){
                String path = str.substring(str.indexOf("-f") + 3,str.indexOf(" ",str.indexOf("-f") + 3));
                body = readFile(path);
            }
            contentLength = String.valueOf(body.length());
        }

        /*initial headers to hash-map*/
        header.put("Host",this.host);
        header.put("Connection",connectionType);
        header.put("User-Agent",userAgent);
        if(allow.equals("POST")) {
            header.put("Content-Length", contentLength);
            header.put("Content-Type", contentType);
        }

        /*-h Header requirement:support multiple headers add or update*/
        String temp = str;
        String key;
        String value;
        for (int i = 0; i < str.length(); i++) {
            if(!temp.contains("-h")){
                break;
            }else{
                i = temp.indexOf("-h") + 3;
                temp = temp.substring(i);
                key = temp.substring(0,temp.indexOf(":",0));
                value = temp.substring(temp.indexOf(":",temp.indexOf(key))+ 1,temp.indexOf(" ",temp.indexOf(key)));
                if(header.containsKey(key)){
                    header.replace(key,value);
                    continue;
                }
                header.put(key,value);
            }
        }
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append(allow + " " + url + " HTTP/1.0\r\n");
        for (String keys:header.keySet()) {
            stringBuilder.append(keys).append(": ").append(header.get(keys)).append("\r\n");
        }
        if(allow.equals("POST")){
            stringBuilder.append("\r\n").append(body);
        }else if(allow.equals("GET")){
            stringBuilder.append("\r\n");
        }
        return stringBuilder.toString();
    }

    private String buildResponse(String payload, String str) throws IOException{



        String response = payload;

        /*verbose requirement*/
        if(str.contains("-v")) {//case that needs verbose
            if(needOutputFile(str)){//case need to output body data
                writeFile(response,str.substring(str.indexOf("-o") + 3));
            }
            return response;
        }else {//case that does not need verbose
            response = response.substring(response.indexOf("\r\n\r\n"));
            if(needOutputFile(str)){//case need to output body data
                writeFile(response,str.substring(str.indexOf("-o") + 3));
            }
        }
        return response;
    }
}
