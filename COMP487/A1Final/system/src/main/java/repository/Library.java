package repository;

import model.Book;

import javax.servlet.ServletContext;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public class Library{

    private static Library library;
    private ConcurrentMap<Integer, Book> map;
    private AtomicInteger mapKey;

    private Library(){
        mapKey = new AtomicInteger();
        map = new ConcurrentHashMap<>();
        Book book1 = new Book("Computer Networking", "Seventh edition",
                "0133594149", "Kurose", "Pearson Education");
        Book book2 = new Book("Computer Vision", "September 3, 2010 draft",
                "1131665258", "Richard Szeliski", "Springer");
        Book book3 = new Book("Data Structure", "Sixth Edition",
                "9781118771334", "Michael", "JohnWiley & Sons");
        addBook(book1);
        addBook(book2);
        addBook(book3);
    }

    public static Library getLibrary() {
        if (library == null) {
            library = new Library();
        }
        return library;
    }

    public ConcurrentMap<Integer, Book> getMap(){
//        if(getServletContext()==null) return null;
        return this.map;
    }

    public int addBook(Book book) {
        int id = mapKey.incrementAndGet();
        book.setId(id);
        map.put(id, book);
        return id;
    }

    public Book getBook(int id){
        return map.get(id);
    }

    public List<Book> getAllBooks() {
        return new ArrayList<>(map.values());
    }

    public int updateBook(Book book){
        Book updatedBook = map.replace(book.getId(),book);
        return updatedBook.getId();
    }

    public int removeBook(int id){
        Book removedBook = map.remove(id);
        return removedBook.getId();
    }

}
