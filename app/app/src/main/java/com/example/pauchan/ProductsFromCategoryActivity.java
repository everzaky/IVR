package com.example.pauchan;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Paint;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.io.File;
import java.util.Map;

public class ProductsFromCategoryActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.products_from_categories);
        Bundle arguments = getIntent().getExtras();
        TextView menu = (TextView) findViewById(R.id.menu);
        menu.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(ProductsFromCategoryActivity.this, MenuActivity.class);
                startActivity(intent);
            }
        });
        if (arguments != null){
            String[] names = arguments.getStringArray("names");
            String[] paths = arguments.getStringArray("paths");
            Integer[] ids = (Integer[]) arguments.get("ids");
            Double[] prices = (Double[]) arguments.get("prices");
            Double[] sales = (Double[]) arguments.get("sales");
            Boolean[] is_sale = (Boolean[]) arguments.get("is_sale");
            LinearLayout linearLayout = (LinearLayout) findViewById(R.id.product_Lin_layout);
            LayoutInflater layoutInflater = getLayoutInflater();
            for (int i = 0; i< names.length; i++){
                View item = layoutInflater.inflate(R.layout.product, linearLayout, false);
                TextView name = (TextView) item.findViewById(R.id.name_of_product);
                name.setText(names[i]);
                TextView price = (TextView) item.findViewById(R.id.product_price);
                TextView sale = (TextView) item.findViewById(R.id.product_price_sale);
                if (is_sale[i]){
                    price.setText(prices[i].toString());
                    price.setPaintFlags(price.getPaintFlags()| Paint.STRIKE_THRU_TEXT_FLAG);
                    sale.setText(sales[i].toString());
                }else{
                    price.setText(prices[i].toString());
                }
                ImageView imageView = (ImageView) item.findViewById(R.id.product_img);
                Bitmap mb = BitmapFactory.decodeFile(paths[i]);
                imageView.setImageBitmap(mb);
                final Button button = (Button) item.findViewById(R.id.search_add_busket);
                button.setTag(ids[i].toString());
                button.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        String id = (String) button.getTag();
                        Map<String, Integer> m = ((MyApplication) getApplication()).getM();
                        boolean b = false;
                        for (Map.Entry<String, Integer> me: m.entrySet()){
                            if (id.equals(me.getKey())){
                                b = true;
                            }
                        }
                        if (b){
                            m.put(id, m.get(id)+1);
                        }else{
                            m.put(id, 1);
                        }
                        ((MyApplication) getApplication()).setM(m);
                    }
                });
                linearLayout.addView(item);
            }
        }
    }
}
