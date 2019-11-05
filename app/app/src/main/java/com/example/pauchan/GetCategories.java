package com.example.pauchan;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.util.Log;
import android.widget.TextView;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.HashMap;

import static androidx.core.content.ContextCompat.startActivity;

public class GetCategories extends AsyncTask<String, Void, String> {
    private String[] names;
    private Integer[] numbers;
    private Context context;

    public  GetCategories(Context context){
        this.context=context;
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

                JSONArray jsonArray1 = new JSONArray(jsono.getString("categories_names"));
                names = new String[jsonArray1.length()];
                for (int i = 0; i<jsonArray1.length(); i++){
                    names[i]=(String)jsonArray1.get(i);
                }
                JSONArray jsonArray2 = new JSONArray(jsono.getString("categories_numbers"));
                numbers = new Integer[jsonArray2.length()];
                for (int i = 0; i<jsonArray2.length(); i++){
                    numbers[i]=(Integer)jsonArray2.get(i);
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
            Intent intent = new Intent(context, CategoriesActivity.class);
            intent.putExtra("names", names);
            intent.putExtra("numbers", numbers);
            startActivity(context,intent, null);
        }
    }
}

