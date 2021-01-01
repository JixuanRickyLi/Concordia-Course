package com.jixuanli.soen387.repository.core;
import java.awt.*;
import java.sql.*;
import java.util.Arrays;
import java.util.Scanner;


public class Core {

    Connection myConn = null;
    Statement stmt = null;
    ResultSet rs = null;

    public Core(){
        super();
        connection();
    }

    public void connection(){

        String user = "root";
        String pwd = "Ricky.123";
        String host = "jdbc:mysql://localhost:3306/BookSchema";

        try{
            Class.forName("com.mysql.cj.jdbc.Driver");
            myConn = DriverManager.getConnection(host,user,pwd);
            stmt = myConn.createStatement();
        }

        catch (Exception e){
            System.out.println(Arrays.toString(e.getStackTrace()));
        }

    }


    public Book[] list_all_books() {
        ResultSet rs = null;
        int size = 0;
        try {
            rs = stmt.executeQuery("SELECT * FROM BOOK");
            if (rs != null)
            {
                    rs.beforeFirst();
                    rs.last();
                    size = rs.getRow();
                    rs.beforeFirst();
            }
            Book[] myBooks = new Book[size];
            int i = 0;
            int id = 0;

            
            String title = null;
            String description = null;
            String isbn = null;
            String publisher = null;
            String cover = null;
            String author = null;

            while(rs.next()){
                id = rs.getInt(1);
                title = rs.getString(2);
                description = rs.getString(3);
                isbn = rs.getString(4);
                publisher = rs.getString(5);
                cover = rs.getString(6);
                author = rs.getString(7);

                Book myBook = new Book(id,title,description,isbn,publisher,cover,author);
                myBooks[i++] = myBook;
            }

            return myBooks;

        }
        catch (Exception e){
            System.out.print(e);
        }


    return new Book[0];

    }

    public Book get_book(int iD) {
        ResultSet rs = null;
        int id = 0;

        String title = null;
        String description = null;
        String isbn = null;
        String publisher = null;
        String cover = null;
        String author = null;

        Book myBook = null;
        try {
            String query = "SELECT * FROM BOOK WHERE id = ?";
            PreparedStatement ps= myConn.prepareStatement(query);
            ps.setInt(1,iD);
            rs = ps.executeQuery();

                while(rs.next()) {
                    id = rs.getInt(1);
                    title = rs.getString(2);
                    description = rs.getString(3);
                    isbn = rs.getString(4);
                    publisher = rs.getString(5);
                    cover = rs.getString(6);
                    author = rs.getString(7);
                    myBook = new Book(id, title, description, isbn, publisher, cover, author);
                }


        }
        catch (Exception e){
            System.out.println(e);
        }

        return myBook;
    }

    public Book get_book(String iSBN) {
        Book myBook = null;
        int id = 0;

        String title = null;
        String description = null;
        String isbn = null;
        String publisher = null;
        String cover = null;
        String author = null;
        ResultSet rs = null;


        try {
            PreparedStatement pss= myConn.prepareStatement("SELECT * FROM BOOK WHERE isbn = ?");
            pss.setString(1, iSBN);
            rs = pss.executeQuery();

            while(rs.next()){

                id = rs.getInt(1);
                title = rs.getString(2);
                description = rs.getString(3);
                isbn = rs.getString(4);
                publisher = rs.getString(5);
                cover = rs.getString(6);
                author = rs.getString(7);
                myBook = new Book(id,title,description,isbn,publisher,cover,author);}
        }
        catch (Exception e){
            System.out.println(e);
        }
        return myBook;
    }

    public int add_new (String title, String des, String iSBN, String publisher, String cover, String author) {

        int iD = 0;
        Book myBook = null;
        String query = "Select max(id) From book";
        try {
            rs = stmt.executeQuery(query);
            while (rs.next()) {
                iD = rs.getInt("max(iD)");
            }
            iD++;

            PreparedStatement pss= myConn.prepareStatement("INSERT INTO BOOK VALUES(?,?,?,?,?,?,?)");
            pss.setInt(1, iD);
            pss.setString(2,title);
            pss.setString(3,des);
            pss.setString(4,iSBN);
            pss.setString(5,publisher);
            pss.setString(6,cover);
            pss.setString(7,author);
            pss.executeUpdate();

        }
        catch (Exception e){
            System.out.print(e);
        }
        return iD;
    }

    public void update_books(){

    }

    public void set_cover(){

    }

    public void delete_a_book(int iD){

    }

    public void delete_all(){

    }


}
