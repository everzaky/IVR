package com.example.pauchan;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.util.Log;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

import static androidx.core.content.ContextCompat.startActivity;

public class Save_img extends AsyncTask<String, Void, String> {
    private Context context;
    private Context con;
    private Integer[] ids;
    private String[] names;
    private Double[] prices;
    private Boolean[] is_sale;
    private String[] images;
    private Double[] sales;
    private File[] paths;
    private String type;
    private String to;
    public Save_img(Context con, String[] images,  File[] paths, Context context, Integer[] ids, String[] names, Double[] prices, Boolean[] is_sale, Double[] sales, String type, String to){
        this.con = con;
        this.images = images;
        this.paths = paths;
        this.ids = ids;
        this.names = names;
        this.prices = prices;
        this.context=context;
        this.is_sale=is_sale;
        this.sales = sales;
        this.type = type;
        this.to = to;
    }

    @Override
    protected String doInBackground(String... strings) {

        try{
            for (int i = 0; i<images.length; i++){
                if (!paths[i].exists() && ids[i]!=-1){
                    String urler = ((MyApplication) con).getProtocol()+((MyApplication) con).getWebsite()+":"+((MyApplication) con).getPort()+"/android/get/"+type+"/picture/"+images[i];
                    Log.d("", urler);
                    URL url = new URL(urler);
                    HttpURLConnection connection = (HttpURLConnection) url
                            .openConnection();
                    connection.setRequestMethod("GET");
                    connection.connect();
                    File file = paths[i];
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
            }
            return "OK";
        } catch (Exception e){
            Log.d("TAG", " "+e.getMessage());
            e.printStackTrace();
        }
        return "Problem";
    }

    @Override
    protected void onPostExecute(String s){
        if (s.equals("OK")){
            Intent intent;
            if (to.equals("Category")) {
                intent = new Intent(context, ProductsFromCategoryActivity.class);
            }else{
                intent = new Intent(context, BusketActivity.class);
            }
            for (int i = 0; i<images.length; i++){
                images[i]=paths[i].getPath();
            }
            intent.putExtra("paths", images);
            intent.putExtra("ids", ids);
            intent.putExtra("prices", prices);
            intent.putExtra("is_sale", is_sale);
            intent.putExtra("sales",sales);
            intent.putExtra("names", names);
            startActivity(context, intent,null);
        }
    }

}
