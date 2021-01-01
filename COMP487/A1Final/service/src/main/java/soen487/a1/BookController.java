package soen487.a1;

import model.Book;
import repository.Library;

import javax.servlet.ServletContext;
import javax.ws.rs.*;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import java.util.List;
import java.util.concurrent.ConcurrentMap;

@Path("/book")
public class BookController {

//    @Context
//    private ServletContext servletContext;

    private Library library = Library.getLibrary();

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    @Path("/list")
    public String list() {
        List<Book> books = library.getAllBooks();
        return books.toString();
    }

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    @Path("/{id}")
    public String getBook(@PathParam("id") int id) {
        Book book = library.getBook(id);
        return book.toString();
    }

    @POST
    @Produces(MediaType.TEXT_PLAIN)
//    @Path("/")
    public String addBook(@QueryParam("title") String title,
                          @QueryParam("description") String description,
                          @QueryParam("isbn") String isbn,
                          @QueryParam("author") String author,
                          @QueryParam("publisher") String publisher) {
        Book book = new Book(title, description, isbn, author, publisher);
        library.addBook(book);
        return book.toString();
    }

    @PUT
    @Produces(MediaType.TEXT_PLAIN)
//    @Path("/")
    public String updateBook(@QueryParam("title") String title,
                            @QueryParam("description") String description,
                            @QueryParam("isbn") String isbn,
                            @QueryParam("author") String author,
                            @QueryParam("publisher") String publisher,
                             @QueryParam("id") int id) {
        Book newBook = new Book(title, description, isbn, author, publisher);
        ConcurrentMap<Integer, Book> map = library.getMap();
        Book book = map.get(id);
        if (book == null) {
            return "Book not found";
        }
        newBook.setId(id);
        library.updateBook(newBook);
        return newBook.toString();
    }

    @DELETE
    @Produces(MediaType.TEXT_PLAIN)
    @Path("/{id}")
    public String deleteBook(@PathParam("id") int id) {
        int i = library.removeBook(id);
        return "Book " + i + " is deleted";
    }

}
