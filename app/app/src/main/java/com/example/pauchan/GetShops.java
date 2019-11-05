package com.example.pauchan;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONObject;

import static androidx.core.content.ContextCompat.startActivity;


public class GetShops  extends AsyncTask<String, Void, String> {
    private Integer[] ids;
    private String[] names;
    private Context context;
    private Context con;

    public GetShops(Context con, Context context){
        this.con  = con;
        this.context = context;
    }

    @Override
    protected String doInBackground(String... strings) {
        try{
            String url = ((MyApplication) con).getProtocol()+((MyApplication) con).getWebsite()+":"+((MyApplication) con).getPort()+"/android/get/shops";
            HttpGet httppost = new HttpGet(url);
            HttpClient httpclient = new DefaultHttpClient();
            HttpResponse response = httpclient.execute(httppost);
            int status = response.getStatusLine().getStatusCode();
            if (status == 200) {
                HttpEntity entity = response.getEntity();
                String data = EntityUtils.toString(entity);
                JSONObject jsono = new JSONObject(data);
                JSONArray jsonArray = jsono.getJSONArray("ids");
                ids = new Integer[jsonArray.length()];
                for (int i = 0; i<jsonArray.length(); i++){
                    ids[i]=(Integer) jsonArray.get(i);
                }
                JSONArray jsonArray1 = jsono.getJSONArray("names");
                names = new String[jsonArray1.length()];
                for (int i = 0; i<jsonArray1.length(); i++){
                    names[i]=(String) jsonArray1.get(i);
                }
                return "OK";
            }
            return "Problem";
        }catch (Exception e){
            e.printStackTrace();
        }
        return "Problem";
    }

    @Override
    protected void onPostExecute(String s) {
        super.onPostExecute(s);
        if (s.equals("OK")){
            Intent intent = new Intent(context, ChooseShopActivity.class);
            intent.putExtra("ids", ids);
            intent.putExtra("names", names);
            startActivity(context, intent,null);
        }
    }

}
