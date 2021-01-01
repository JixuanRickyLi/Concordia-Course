package com.jixuanli.soen387.repository.core;

public class Session {
    public void getCurrentUser(){

    }

    public boolean isUserLoggedIn(){
        return true;
    }

    public boolean login(int userID, String pwd){

        return true;
    }

    public boolean logout(){

        return true;
    }

    //login through users.json stored somewhere.
    //the path stored in a config file
    //pwds are stored in MD5 hashes.

}
