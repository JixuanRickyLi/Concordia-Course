package com.jixuanli.soen387.repository.core;

import java.awt.*;

public class Book {

    private int iD;
    private String iSBN;
    private  String title;
    private  String description;
    private String publisher;
    private  String cover;
    private String author;

    public Book(int iD, String iSBN,String title, String description, String publisher, String cover , String author){
        this.iD = iD;
        this.title = title;
        this.description = description;
        this.iSBN = iSBN;
        this.publisher = publisher;
        this.cover = cover;
        this.author = author;
    }


    public int getiD() {
        return iD;
    }

    public void setiD(int iD) {
        this.iD = iD;
    }

    public String getiSBN() {
        return iSBN;
    }

    public void setiSBN(String iSBN) {
        this.iSBN = iSBN;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getCover() {
        return cover;
    }

    public void setCover(String cover) {
        this.cover = cover;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public String getPublisher() {
        return publisher;
    }

    public void setPublisher(String publisher) {
        this.publisher = publisher;
    }
}
