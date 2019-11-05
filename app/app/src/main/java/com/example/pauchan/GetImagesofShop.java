package com.example.pauchan;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class GetImagesofShop extends AsyncTask<String, Void, String> {
    Context context;
    Context con;
    String[] shop_images;
    File[] paths;
    Integer id;

    public GetImagesofShop(Integer id,Context context, Context con, String[] shop_images, File[] paths){
        this.context=context;
        this.con=con;
        this.id=id;
        this.shop_images=shop_images;
        this.paths=paths;
    }

    @Override
    protected String doInBackground(String... strings) {
        try {
            for (int i = 0; i<shop_images.length;  i++){
                if (!paths[i].exists()) {
                    String urler = ((MyApplication) con).getProtocol() + ((MyApplication) con).getWebsite() + ":" + ((MyApplication) con).getPort() + "/android/get/shop/picture/" + id.toString() + "/" + shop_images[i];
                    Log.d("", urler);
                    URL url = new URL(urler);
                    HttpURLConnection connection = (HttpURLConnection) url
                            .openConnection();
                    connection.setRequestMethod("GET");
                    connection.connect();
                    File file = paths[i];
                    InputStream inputStream = connection.getInputStream();
                    FileOutputStream fileOutput = new FileOutputStream(file);
                    int totalSize = connection.getContentLength();
                    int downloadedSize = 0;
                    byte[] buffer = new byte[1024];
                    int bufferLength = 0;
                    while ((bufferLength = inputStream.read(buffer)) > 0) {
                        fileOutput.write(buffer, 0, bufferLength);
                        downloadedSize += bufferLength;
                    }
                    fileOutput.close();
                }
            }
            return "OK";
        }catch (Exception e){
            e.printStackTrace();
        }
        return "Problem";
    }


    @Override
    protected void onPostExecute(String s) {
        super.onPostExecute(s);
        if (s.equals("OK")){
            new GetProductShop(con, context, shop_images, id).execute("fassaf");
        }
    }

}
