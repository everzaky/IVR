package com.example.pauchan;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Space;
import android.widget.Spinner;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class ChooseShopActivity extends AppCompatActivity  {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.choose_shop);
        Bundle arguments = getIntent().getExtras();
        if (arguments!=null){
            String[] names = arguments.getStringArray("names");
            final Integer[] ids = (Integer[]) arguments.get("ids");
            Button button = (Button) findViewById(R.id.button_choose_shop);
            final Spinner spinner = (Spinner) findViewById(R.id.choose_shop);
            ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, names);
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
            spinner.setAdapter(adapter);
            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Log.d("ff", (ids[(Integer)spinner.getSelectedItemPosition()]).toString()+" ");
                    new GetShop(ids[spinner.getSelectedItemPosition()], getApplicationContext(), ChooseShopActivity.this).execute("fff");
                }
            });
        }
    }

}
