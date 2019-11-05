package com.example.pauchan;

import android.app.Activity;
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
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import static androidx.core.content.ContextCompat.startActivity;

public class EstablishConnectionTask extends AsyncTask<String, Void, String> {
    public TextView textView;
    public String login;
    public Context act;
    public Context context;

    public EstablishConnectionTask(TextView textView, String login, Context act, Context context){
        this.textView = textView;
        this.login=login;
        this.act = act;
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
                return  jsono.getString("answer");

            }else{
                return "Hack";
            }

        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return "";
    }

    @Override
    protected void onPostExecute(String s) {
        super.onPostExecute(s);
        if (s.equals("OK")) {
            ((MyApplication) act).setUsername(login);
            ((MyApplication) act).setM(new HashMap<String, Integer>());
            Intent intent = new Intent(context, MenuActivity.class);
            startActivity(context, intent, null);
        } else {
                if (s.equals("Problem")) {
                    textView.setText("Неправильный пароль/догин");
                } else {
                    if (s.equals("HACK")) {
                        textView.setText("Что-то пошло не так");
                    } else {
                        textView.setText(s);
                    }
                }
            }
    }
}
