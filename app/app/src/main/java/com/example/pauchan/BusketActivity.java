package com.example.pauchan;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Paint;
import android.os.Bundle;
import android.text.Layout;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import java.util.Map;

public class BusketActivity extends AppCompatActivity {
    private TextView menu;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.busket);
        menu = (TextView) findViewById(R.id.menu);
        Bundle arguments = getIntent().getExtras();
        menu.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(BusketActivity.this, MenuActivity.class);
                startActivity(intent);
            }
        });
        if (arguments != null) {
            String[] names = arguments.getStringArray("names");
            String[] paths = arguments.getStringArray("paths");
            Integer[] ids = (Integer[]) arguments.get("ids");
            Double[] prices = (Double[]) arguments.get("prices");
            Double[] sales = (Double[]) arguments.get("sales");
            Boolean[] is_sale = (Boolean[]) arguments.get("is_sale");
            LinearLayout linearLayout = (LinearLayout) findViewById(R.id.busket_linear_layout);
            LayoutInflater layoutInflater = getLayoutInflater();
            Map<String, Integer> m = ((MyApplication) getApplication()).getM();
            for (int i = 0; i < names.length; i++) {
                if (ids[i] != -1) {
                    View item = layoutInflater.inflate(R.layout.product_busket, linearLayout, false);
                    TextView name = (TextView) item.findViewById(R.id.busket_product_name);
                    name.setText(names[i]);
                    TextView price = (TextView) item.findViewById(R.id.busket_price);
                    TextView sale = (TextView) item.findViewById(R.id.busket_sale_price);
                    if (is_sale[i]) {
                        price.setText(prices[i].toString());
                        price.setPaintFlags(price.getPaintFlags() | Paint.STRIKE_THRU_TEXT_FLAG);
                        sale.setText(sales[i].toString());
                    } else {
                        price.setText(prices[i].toString());
                    }
                    ImageView imageView = (ImageView) item.findViewById(R.id.busket_product_img);
                    Bitmap mb = BitmapFactory.decodeFile(paths[i]);
                    imageView.setImageBitmap(mb);
                    TextView number = (TextView) item.findViewById(R.id.busket_number);
                    Log.d("ff", ids[i].toString());
                    Integer numb=0;
                    for (Map.Entry<String, Integer> me: m.entrySet()){
                        Log.d("ffasfa", me.getKey()+" "+me.getValue().toString());
                        if (me.getKey().equals(ids[i].toString())){
                            numb = me.getValue();
                        }
                    }
                    number.setText(numb.toString());
                    number.setTag(ids[i].toString());
                    final TextView add = (TextView) item.findViewById(R.id.busket_add);
                    add.setTag(ids[i].toString());
                    final TextView reduce = (TextView) item.findViewById(R.id.busket_reduce);
                    reduce.setTag(ids[i].toString());
                    add.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View view) {
                            Log.d("ff", "ff");
                            String id = (String) add.getTag();
                            LinearLayout linearLayout = (LinearLayout) findViewById(R.id.busket_linear_layout);
                            Integer kol = linearLayout.getChildCount();
                            for (int i = 0; i<kol; i++){
                                ConstraintLayout lt = (ConstraintLayout)linearLayout.getChildAt(i);
                                final TextView numb = (TextView) lt.getChildAt(3);
                                if (((String) numb.getTag()).equals(id)){
                                    Map<String, Integer> m = ((MyApplication) getApplication()).getM();
                                    Integer number=0;
                                    for (Map.Entry<String, Integer> me: m.entrySet()){
                                        Log.d("ffasfa", me.getKey()+" "+me.getValue().toString());
                                        if (me.getKey().equals(id)){
                                            number = me.getValue();
                                        }
                                    }
                                    number+=1;
                                    m.put(id, number);
                                    try{
                                        numb.setText(number.toString());
                                    }catch (Exception e){
                                        e.printStackTrace();
                                    }
                                }
                            }
                        }
                    });
                    reduce.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View view) {
                            String id = (String) reduce.getTag();
                            LinearLayout linearLayout = (LinearLayout) findViewById(R.id.busket_linear_layout);
                            Integer kol = linearLayout.getChildCount();
                            Integer kek = 0;
                            for (int i = 0; i<kol; i++){
                                ConstraintLayout lt = (ConstraintLayout)linearLayout.getChildAt(i);
                                final TextView numb = (TextView) lt.getChildAt(3);
                                if (((String) numb.getTag()).equals(id)){
                                    kek=i;
                                }
                            }
                            Map<String, Integer> m = ((MyApplication) getApplication()).getM();
                            Integer number=0;
                            for (Map.Entry<String, Integer> me: m.entrySet()){
                                Log.d("ffasfa", me.getKey()+" "+me.getValue().toString());
                                if (me.getKey().equals(id)){
                                    number = me.getValue();
                                }
                            }
                            if (number==1){
                                linearLayout.removeViewAt(kek);
                                m.remove(id);
                            }else{
                                number -=1;
                                ConstraintLayout lt = (ConstraintLayout)linearLayout.getChildAt(kek);
                                final TextView numb = (TextView) lt.getChildAt(3);
                                m.put(id, number);
                                try{
                                    numb.setText(number.toString());
                                }catch (Exception e){
                                    e.printStackTrace();
                                }
                            }

                        }
                    });
                    linearLayout.addView(item);
                }
            }
        }
    }
}
