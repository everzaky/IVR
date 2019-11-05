package com.example.pauchan;

import android.content.Context;
import android.os.AsyncTask;
import android.os.Environment;

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
import java.util.Map;

public class GetProductsFromBusket extends AsyncTask<String, Void, String> {

    private Context context;
    private Context con;
    private String[] kek;
    private Integer[] ids;
    private String[] names;
    private Double[] prices;
    private Boolean[] is_sale;
    private String[] images;
    private Double[] sales;
    private Integer kol;

    public  GetProductsFromBusket(Context context, Context con){
        this.context=context;
        this.con = con;
        Map<String, Integer> m = ((MyApplication) con).getM();
        this.kol = m.size();
        this.ids = new Integer[kol];
        this.names = new String[kol];
        this.prices = new Double[kol];
        this.is_sale = new Boolean[kol];
        this.images = new String[kol];
        this.sales  = new Double[kol];
        this.kek = new String[kol];
        Integer i = 0;
        for (Map.Entry<String, Integer> me :m.entrySet()){
            kek[i]=me.getKey();
            i+=1;
        }
    }

    @Override
    protected String doInBackground(String... strings) {
        try{
            for (int i = 0; i<kol; i++){
                String url = ((MyApplication) con).getProtocol()+((MyApplication) con).getWebsite()+":"+((MyApplication) con).getPort()+"/android/get/product/"+kek[i];
                HttpGet httppost = new HttpGet(url);
                HttpClient httpclient = new DefaultHttpClient();
                HttpResponse response = httpclient.execute(httppost);
                int status = response.getStatusLine().getStatusCode();
                if (status==200){
                    HttpEntity entity = response.getEntity();
                    String data = EntityUtils.toString(entity);
                    JSONObject jsono = new JSONObject(data);

                    ids[i]=(Integer)jsono.getInt("id");
                    names[i]=(String)jsono.getString("name");
                    prices[i]=(Double) jsono.getDouble("price");
                    sales[i]=(Double) jsono.getDouble("sale");
                    is_sale[i] = (Boolean) jsono.getBoolean("is_sale");
                    images[i] = (String) jsono.getString("image");
                }else{
                    ids[i]=-1;
                }
            }
            return "OK";
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
            for (int i = 0; i<images.length; i++) {
                if (ids[i] != -1) {
                    paths[i] = Work_with_images.getOutputMediaFile(images[i], con, "product");
                }
            }
            new Save_img(con, images, paths,context, ids, names, prices, is_sale, sales, "product", "Busket").execute("kek");
        }
    }


}
