package com.example.pauchan;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.util.Log;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.File;

import static androidx.core.content.ContextCompat.startActivity;

public class GetShop extends AsyncTask<String, Void, String> {

    private Integer id;
    private Context context;
    private Context con;
    private String[] shop_images;
    public GetShop(Integer id, Context con, Context context){
        this.id=id;
        this.con = con;
        this.context=context;
    }

    @Override
    protected String doInBackground(String... strings) {
        try {
            String url = ((MyApplication) con).getProtocol()+((MyApplication) con).getWebsite()+":"+((MyApplication) con).getPort()+"/android/get/shop/"+id.toString();
            HttpGet httppost = new HttpGet(url);
            HttpClient httpclient = new DefaultHttpClient();
            HttpResponse response = httpclient.execute(httppost);
            int status = response.getStatusLine().getStatusCode();
            if (status == 200) {
                HttpEntity entity = response.getEntity();
                String data = EntityUtils.toString(entity);
                JSONObject jsono = new JSONObject(data);
                JSONArray jsonArray = jsono.getJSONArray("images");
                shop_images = new String[jsonArray.length()];
                for (int i = 0; i<jsonArray.length(); i++){
                    shop_images[i]=(String)jsonArray.get(i);
                }
                return "OK";
            }else{
                return "Problem";
            }
        }catch (Exception e){
            e.printStackTrace();
        }

        return "Problem";
    }

    @Override
    protected void onPostExecute(String s) {
        super.onPostExecute(s);
        if (s.equals("OK") && shop_images.length>0){
            Log.d("dsadsad","asdasd");
            File[] paths = new File[shop_images.length];
            for (int i = 0; i<shop_images.length; i++){
                paths[i]=Work_with_images.getOutputMediaFile(shop_images[i], con, "shop");
            }
            new GetImagesofShop(id, context, con, shop_images, paths).execute("ff");
        }
    }
}
