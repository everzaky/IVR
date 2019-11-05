package com.example.pauchan;

import android.app.Activity;
import android.content.Context;
import android.os.AsyncTask;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.AbsoluteLayout;
import android.widget.HorizontalScrollView;
import android.widget.ImageView;
import android.widget.LinearLayout;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONObject;

public class GetLocations extends AsyncTask<String, Void, String> {
    private LinearLayout liner;
    private Context context;
    private Context con;
    private Integer id;
    private String nm_p;
    private ImageView v;
    private AbsoluteLayout[] abs;
    public GetLocations(Context context, Context con, LinearLayout liner, Integer id, String nm_p, ImageView v, AbsoluteLayout[] abs){
        this.con=con;
        this.context=context;
        this.liner = liner;
        this.id = id;
        this.nm_p=nm_p;
        this.v=v;
        this.abs =abs;
    }

    @Override
    protected String doInBackground(String... strings) {
        try {
            String url = ((MyApplication) con).getProtocol()+((MyApplication) con).getWebsite()+":"+((MyApplication) con).getPort()+"android/get/locations/shop/"+id.toString()+"/product/"+nm_p;
            HttpGet httppost = new HttpGet(url);
            HttpClient httpclient = new DefaultHttpClient();
            HttpResponse response = httpclient.execute(httppost);
            int status = response.getStatusLine().getStatusCode();
            if (status == 200) {
                HttpEntity entity = response.getEntity();
                String data = EntityUtils.toString(entity);
                JSONObject jsono = new JSONObject(data);
                JSONArray jsonArray1 = new JSONArray(jsono.getString("width"));
                JSONArray jsonArray2 = new JSONArray(jsono.getString("height"));
                for (int i = 0; i<jsonArray1.length(); i++){
                    Integer[] width = (Integer[]) jsonArray1.get(i);
                    Integer[] height = (Integer[]) jsonArray2.get(i);

                    for (int j = 0; j<width.length; j++){
                       // AbsoluteLayout absoluteLayout = (AbsoluteLayout) ((HorizontalScrollView) liner.getChildAt(0)).getChildAt(0);

                    }
                }
            }

        }catch (Exception e){
            e.printStackTrace();
        }
        return "OK";
    }
}
