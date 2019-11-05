package com.example.pauchan;

import android.content.Context;
import android.graphics.Bitmap;
import android.os.Environment;
import android.util.Log;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

public class Work_with_images {
    public static File getOutputMediaFile(String name, Context con, String type){
        File mediaStorageDir = new File(Environment.getExternalStorageDirectory()+"/Android/data/"+con.getPackageName()+"/Files");
        if (!mediaStorageDir.exists()){
            if (!mediaStorageDir.mkdirs()){
                return null;
            }
        }
        File mediaFile;
        if (type.equals("product")) {
            mediaFile = new File(mediaStorageDir.getPath() + File.separator + "product"+name);
        }else {
            mediaFile = new File(mediaStorageDir.getPath() + File.separator + "shop"+name);
        }
        return mediaFile;
    }

}
