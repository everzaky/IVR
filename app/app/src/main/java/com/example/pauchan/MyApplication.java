package com.example.pauchan;

import android.app.Application;

import java.util.HashMap;
import java.util.Map;

public class MyApplication extends Application {
    private String website="192.168.100.26";
    private String port ="5000";
    private String protocol = "http://";
    private String username;
    private Map<String, Integer> m = new HashMap<>();

    public String getWebsite(){
        return website;
    }

    public String getPort(){
        return port;
    }

    public void setWebsite(String website){
        this.website = website;
    }

    public void setPort(String port){
        this.port = port;
    }

    public String getProtocol(){
        return protocol;
    }

    public void setProtocol(String protocol){
        this.protocol=protocol;
    }

    public Map<String,Integer> getM() {
        return m;
    }

    public void setM(Map<String, Integer> m){
        this.m = m;
    }


    public String getUsername(){
        return username;
    }

    public void setUsername(String username){
        this.username=username;
    }


}
