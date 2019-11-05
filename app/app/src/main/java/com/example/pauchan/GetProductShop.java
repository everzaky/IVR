package com.example.pauchan;

import android.annotation.SuppressLint;
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
import java.io.StringReader;
import java.util.Map;

import static androidx.core.content.ContextCompat.startActivity;

public class GetProductShop extends AsyncTask<String, Void, String> {
    private Context context;
    private Context con;
    private String[] shop_images;
    private Integer id;
    private String[] names;
    private String[] product_images;
    private Integer[] ids;
    private Integer[] numbers;
    private Boolean[] is_sale;
    private Double[] sales;
    private Double[] prices;
    private Integer[] number_to_buy;

    public GetProductShop(Context con, Context context, String[] shop_images, Integer id){
        this.con = con;
        this.context=context;
        this.shop_images=shop_images;
        this.id=id;
    }



    @SuppressLint("WrongThread")
    @Override
    protected String doInBackground(String... strings) {
        try {

            Map<String, Integer> m = ((MyApplication) con).getM();
            names = new String[m.size()];
            ids = new Integer[m.size()];
            numbers = new Integer[m.size()];
            product_images = new String[m.size()];
            is_sale = new Boolean[m.size()];
            prices = new Double[m.size()];
            sales = new Double[m.size()];
            number_to_buy = new Integer[m.size()];
            Integer i = 0;
            for (Map.Entry<String, Integer> me: m.entrySet()){
                String url =  ((MyApplication) con).getProtocol() + ((MyApplication) con).getWebsite() + ":" + ((MyApplication) con).getPort()+"/android/get/product/shop/"+id.toString()+"/product/"+me.getKey();
                HttpGet httppost = new HttpGet(url);
                HttpClient httpclient = new DefaultHttpClient();
                HttpResponse response = httpclient.execute(httppost);
                int status = response.getStatusLine().getStatusCode();
                if (status == 200) {
                    HttpEntity entity = response.getEntity();
                    String data = EntityUtils.toString(entity);
                    JSONObject jsono = new JSONObject(data);
                    names[i]=(String) jsono.get("name");
                    ids[i]=(Integer) jsono.get("id");
                    product_images[i]=(String) jsono.get("image");
                    numbers[i]=(Integer) jsono.get("number");
                    is_sale[i]=(Boolean) jsono.get("is_sale");
                    prices[i]=(Double) jsono.get("price");
                    sales[i]=(Double) jsono.get("sale");
                    number_to_buy[i]=me.getValue();
                    AsyncTask<String, Void, String> asdads = new SaveImg(con, product_images[i]);
                    asdads.execute("asdasdas");
                    i+=1;
                }else{
                    return "Problem";
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
            Intent intent= new Intent(context, BuyingActivity.class);
            intent.putExtra("id", id);
            intent.putExtra("names", names);
            intent.putExtra("numbers", numbers);
            intent.putExtra("ids", ids);
            intent.putExtra("shop_images", shop_images);
            intent.putExtra("images", product_images);
            intent.putExtra("is_sale", is_sale);
            intent.putExtra("prices", prices);
            intent.putExtra("sales", sales);
            intent.putExtra("number_to_buy", number_to_buy);
            startActivity(context, intent, null);
        }
    }
}
