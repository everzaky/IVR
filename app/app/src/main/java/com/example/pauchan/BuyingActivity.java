package com.example.pauchan;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.AbsoluteLayout;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.HorizontalScrollView;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

public class BuyingActivity extends AppCompatActivity {

    Integer kol;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.buying);
        Bundle argumetns = getIntent().getExtras();
        if (argumetns!=null){
            Integer id = (Integer) argumetns.get("id");
            Integer [] ids = (Integer[]) argumetns.get("ids");
            String[] names = (String[]) argumetns.get("names");
            Double[] prices = (Double[]) argumetns.get("prices");
            Double[] sales = (Double[]) argumetns.get("sales");
            Boolean[] is_sale = (Boolean[]) argumetns.get("is_sale");
            Integer[] numbers = (Integer[]) argumetns.get("numbers");
            String[] shop_images = (String[]) argumetns.get("shop_images");
            String[] product_images = (String[]) argumetns.get("images");
            Integer[] number_to_buy = (Integer[]) argumetns.get("number_to_buy");
            final LinearLayout linearLayout = (LinearLayout) findViewById(R.id.lin_buying_product);
            LayoutInflater layoutInflater = getLayoutInflater();
            final LinearLayout linearLayout1 = (LinearLayout) findViewById(R.id.lin_buying_shops);
            kol = ids.length;
            for (int i = 0; i<ids.length; i++){
                View v =layoutInflater.inflate(R.layout.product_for_buiyng, linearLayout, false);
                final TextView name = (TextView) v.findViewById(R.id.buying_product_name);
                name.setText(names[i]);
                name.setTag(ids[i]);
                name.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {

                    }
                });
                ImageView imageView = (ImageView) v.findViewById(R.id.buying_image);
                Log.d("jjjj",Work_with_images.getOutputMediaFile(product_images[i], getApplicationContext(),"product").getPath());
                Bitmap mb = BitmapFactory.decodeFile(Work_with_images.getOutputMediaFile(product_images[i], getApplicationContext(),"product").getPath());
                imageView.setImageBitmap(mb);
                final CheckBox checkBox=(CheckBox) v.findViewById(R.id.buying_check_box);
                checkBox.setOnCheckedChangeListener(new CheckBox.OnCheckedChangeListener(){

                    @Override
                    public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                        if (checkBox.isChecked()) {
                            kol-=1;
                        }else{
                            kol+=1;
                        }
                        if (kol==0){
                            Intent intent = new Intent(BuyingActivity.this, cassa.class);
                            startActivity(intent);
                        }
                    }
                });

                TextView price = (TextView) v.findViewById(R.id.product_price_buying);
                TextView sale = (TextView) v.findViewById(R.id.product_sale_price_buying);
                if (is_sale[i]) {
                    price.setText(prices[i].toString());
                    price.setPaintFlags(price.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);
                    sale.setText(sales[i].toString());
                } else {
                    price.setText(prices[i].toString());
                }

                TextView number = (TextView) v.findViewById(R.id.buying_product_shop_number);
                number.setText(numbers[i].toString());
                if (!(numbers[i]> number_to_buy[i]+10)){
                    number.setTextColor(Color.parseColor("#ff0000"));
                }
                TextView to_buy = (TextView) v.findViewById(R.id.buying_busket_number);
                to_buy.setText(number_to_buy[i].toString());
                linearLayout.addView(v);
            }
            for (int i = 0; i<shop_images.length; i++){
                View v = layoutInflater.inflate(R.layout.buingshop, linearLayout1, false);
                ImageView imageView = (ImageView) v.findViewById(R.id.shop_img);
                Log.d("jjjj",Work_with_images.getOutputMediaFile(shop_images[i], getApplicationContext(),"shop").getPath());
                String kek="";
                String lol = Work_with_images.getOutputMediaFile(shop_images[i], getApplicationContext(),"shop").getPath();
                int kk = lol.lastIndexOf('.');
                kek =lol.substring(1,kk)+".png";
                Bitmap mb = BitmapFactory.decodeFile(lol);
                imageView.setImageBitmap(mb);
                linearLayout1.addView(v);
            }
        }
    }
}
