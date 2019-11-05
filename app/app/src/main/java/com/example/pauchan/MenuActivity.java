package com.example.pauchan;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.HashMap;

public class MenuActivity extends AppCompatActivity{
    private TextView ex;
    private TextView search;
    private TextView categories;
    private TextView start;
    private TextView busket;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);
        ex=(TextView) findViewById(R.id.exit);
        categories = (TextView) findViewById(R.id.categories);
        start = (TextView) findViewById(R.id.start_buiyng);
        busket = (TextView) findViewById(R.id.busket);
        ex.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ((MyApplication) getApplication()).setUsername("");
                ((MyApplication) getApplication()).setM(new HashMap<String, Integer>());
                Intent intent = new Intent(MenuActivity.this, MainActivity.class);
                startActivity(intent);
            }
        });


        categories.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                    String url =((MyApplication) getApplication()).getProtocol()+((MyApplication) getApplication()).getWebsite()+":"+((MyApplication) getApplication()).getPort()+"/android/get/categories";
                    Log.d("LLLL", url);
                    new GetCategories(MenuActivity.this).execute(url);
            }
        });

        busket.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new GetProductsFromBusket(MenuActivity.this, getApplicationContext()).execute("kk");
            }
        });

        start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new GetShops(getApplicationContext() , MenuActivity.this).execute("ll");
            }
        });

    }
}
