package com.example.pauchan;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class SearchActivity extends AppCompatActivity {
    private EditText value;
    private Button btn;
    private TextView error;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search);
        btn = (Button) findViewById(R.id.button);
        value = (EditText) findViewById(R.id.value);
        error = (TextView) findViewById(R.id.error);

        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (value.length() != 0) {
                    String url = ((MyApplication) getApplication()).getProtocol() + ((MyApplication) getApplication()).getWebsite()+":"+((MyApplication) getApplication()).getPort()+"/android/search/"+value.getText();
                    error.setText(url);
                }else{
                    error.setText("Не может быть пустым полем");
                }
            }
        });
    }
}
