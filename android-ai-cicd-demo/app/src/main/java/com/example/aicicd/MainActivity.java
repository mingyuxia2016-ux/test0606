package com.example.aicicd;

import android.app.Activity;
import android.os.Bundle;
import android.widget.LinearLayout;
import android.widget.TextView;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        TextView title = new TextView(this);
        title.setText("Android AI CI/CD Demo");
        title.setTextSize(22);
        title.setPadding(32, 32, 32, 16);

        TextView subtitle = new TextView(this);
        subtitle.setText("Push code to build APK, run tests, and show reports in GitHub Actions.");
        subtitle.setTextSize(16);
        subtitle.setPadding(32, 0, 32, 32);

        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.addView(title);
        layout.addView(subtitle);

        setContentView(layout);
    }
}
