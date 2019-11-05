package com.example.pauchan;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class SaveImg extends AsyncTask<String, Void, String> {

    Context con;
    String name;
    File path;

    public SaveImg(Context con, String name){
        this.name=name;
        this.con=con;
        this.path = Work_with_images.getOutputMediaFile(name, con, "product");
    }


    @Override
    protected String doInBackground(String... strings) {
        try {
            if (!path.exists()){
                String urler = ((MyApplication) con).getProtocol()+((MyApplication) con).getWebsite()+":"+((MyApplication) con).getPort()+"/android/get/product/picture/"+name;
                Log.d("", urler);
                URL url = new URL(urler);
                HttpURLConnection connection = (HttpURLConnection) url
                        .openConnection();
                connection.setRequestMethod("GET");
                connection.connect();
                File file = path;
                InputStream inputStream =  connection.getInputStream();
                FileOutputStream fileOutput = new FileOutputStream(file);
                int totalSize = connection.getContentLength();
                int downloadedSize = 0;
                byte[] buffer = new byte[1024];
                int bufferLength = 0;
                while ( (bufferLength = inputStream.read(buffer)) > 0 ) {
                    fileOutput.write(buffer, 0, bufferLength);
                    downloadedSize += bufferLength;
                }
                fileOutput.close();
            }
            return "OK";
        }catch (Exception e){
            return "Problem";
        }
    }
}
