package client;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class Client {
    public static void main(String[] argv) {

        System.out.println("Welcome to the Client system:");

        while (true) {

            System.out.println("Input the command:");

            Scanner scan = new Scanner(System.in);
            String input = scan.nextLine();
            String [] args = input.split(" ");
            String baseURL = "http://localhost:8080/api/book/";

            if (args[0].equals("-h")) {
                displayHelp();
            } else if (args[0].equals("-l")) {
                sendRequest("GET", baseURL + "list");
//                displayHelp();
            } else if (args[0].equals("-d")) {
                sendRequest("GET", baseURL + args[1]);
//                displayHelp();
            } else if (args[0].equals("-a")) {
                sendRequest("POST", baseURL + "?" + args[1]);
//                displayHelp();
            } else if (args[0].equals("-u")) {
                sendRequest("PUT", baseURL + "?" + args[1]);
//                displayHelp();
            } else if (args[0].equals("-r")) {
                sendRequest("DELETE", baseURL + args[1]);
//                displayHelp();
            } else if (args[0].equals("-q")) {
                System.out.println("Bye Bye!");
                System.exit(0);
            }
        }
    }

    public static void sendRequest(String method, String sentURL){
        try {
            URL url = new URL(sentURL);
            HttpURLConnection conn = (HttpURLConnection)url.openConnection();
            conn.setRequestMethod(method);
            conn.setRequestProperty("Accept", "text/plain");
            if (conn.getResponseCode() != 200) {
                throw new RuntimeException("Fail: HTTP error code: "
                        + conn.getResponseCode());
            }
            BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            String out = br.readLine();
            System.out.println(out);
            conn.disconnect();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void displayHelp() {
        System.out.println("-h  help/about");
        System.out.println("-l  list of all books");
        System.out.println("-d + id display the book info by id");
        System.out.println("-a + info   add the book to system");
        System.out.println("-u + id + info  update the book by id");
        System.out.println("-r + id delete the book by console");
        System.out.println("-q  quit");
    }
}
