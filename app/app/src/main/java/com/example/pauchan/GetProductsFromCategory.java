package com.example.pauchan;

import android.content.Context;
import android.content.ContextWrapper;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Environment;
import android.util.Log;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import static androidx.core.content.ContextCompat.startActivity;

public class GetProductsFromCategory extends AsyncTask<String, Void, String> {

    private Context context;
    private Context con;
    private Integer[] ids;
    private String[] names;
    private Double[] prices;
    private Boolean[] is_sale;
    private String[] images;
    private Double[] sales;

    public GetProductsFromCategory(Context context, Context con){
        this.context = context;
        this.con = con;
    }

    @Override
    protected String doInBackground(String... urls) {
        try {
            HttpGet httppost = new HttpGet(urls[0]);
            HttpClient httpclient = new DefaultHttpClient();
            HttpResponse response = httpclient.execute(httppost);
            int status = response.getStatusLine().getStatusCode();
            if (status == 200) {
                HttpEntity entity = response.getEntity();
                String data = EntityUtils.toString(entity);
                JSONObject jsono = new JSONObject(data);
                Log.d("fff", jsono.getString("ids"));
                JSONArray jsonArray1 = new JSONArray(jsono.getString("ids"));
                ids = new Integer[jsonArray1.length()];
                for (int i = 0; i<jsonArray1.length(); i++){
                    ids[i]=(Integer) jsonArray1.get(i);
                }
                JSONArray jsonArray2 = new JSONArray(jsono.getString("names"));
                names = new String[jsonArray2.length()];
                for (int i = 0; i<jsonArray2.length(); i++){
                    names[i]=(String) jsonArray2.get(i);
                }
                JSONArray jsonArray3 = new JSONArray(jsono.getString("prices"));
                prices = new Double[jsonArray3.length()];
                for (int i = 0; i<jsonArray3.length(); i++){
                    prices[i]=(Double)jsonArray3.get(i);
                }
                JSONArray jsonArray4 = new JSONArray(jsono.getString("is_sale"));
                is_sale = new Boolean[jsonArray4.length()];
                for (int i = 0; i<jsonArray4.length(); i++){
                    is_sale[i] = (Boolean)jsonArray4.get(i);
                }
                JSONArray jsonArray5 = new JSONArray(jsono.getString("sales"));
                sales = new Double[jsonArray5.length()];
                for (int i = 0; i<jsonArray5.length(); i++){
                    sales[i] = (Double) jsonArray5.get(i);
                }
                JSONArray jsonArray6 = new JSONArray(jsono.getString("images"));
                images = new String[jsonArray6.length()];
                for (int i = 0; i<jsonArray6.length(); i++){
                    images[i]=(String) jsonArray6.get(i);
                }
                return "OK";
            }else{
                return "Problem";
            }

        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return "Problem";
    }

    @Override
    protected void onPostExecute(String s) {
        super.onPostExecute(s);
        if (s.equals("OK")){

            File mediaStorageDir = new File(Environment.getExternalStorageState()+"/Android/data/"+con.getPackageName()+"/Files");
            File[] paths = new File[images.length];
            for (int i = 0; i<images.length; i++){
                paths[i]=Work_with_images.getOutputMediaFile(images[i], con,"product");
            }
            new Save_img(con, images, paths,context, ids, names, prices, is_sale, sales, "product", "Category").execute("kek");
        }


    }
}
