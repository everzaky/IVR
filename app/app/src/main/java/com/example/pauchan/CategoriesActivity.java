package com.example.pauchan;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import androidx.appcompat.app.AppCompatActivity;

public class CategoriesActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_categories);
        Bundle arguments = getIntent().getExtras();
        if (arguments!=null){
            String[] names = arguments.getStringArray("names");
            final Integer[] numbers = (Integer[]) arguments.get("numbers");
            ListView listView = findViewById(R.id.list_of_categories);
            ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, names);
            listView.setAdapter(adapter);
            listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                    Log.d("fffff", ((Integer) i).toString());
                    String url = ((MyApplication) getApplication()).getProtocol()+((MyApplication) getApplication()).getWebsite()+":"+((MyApplication) getApplication()).getPort()+"/android/search/category/"+numbers[i].toString();
                    Log.d("url", url);
                    new GetProductsFromCategory(CategoriesActivity.this, getApplicationContext()).execute(url);
                }
            });
        }

    }
}
