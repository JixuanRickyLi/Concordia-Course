import java.io.*;
import java.nio.channels.ServerSocketChannel;


public class httpfs {

    public static void main(String[] args) throws IOException {
        listenAndServe();
    }


    private static void listenAndServe() throws IOException {
        ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
        MultiRequests socketThread = new MultiRequests(serverSocketChannel);
        socketThread.start();
    }
}
