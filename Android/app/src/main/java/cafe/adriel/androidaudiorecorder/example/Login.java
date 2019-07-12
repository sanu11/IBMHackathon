package cafe.adriel.androidaudiorecorder.example;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.Button;
import android.view.View.OnClickListener;
import android.widget.EditText;
import android.content.Intent;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.concurrent.ExecutionException;


public class Login extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Button clickButton = (Button) findViewById(R.id.btn_login);
        clickButton.setOnClickListener( new OnClickListener() {

            @Override
            public void onClick(View v) {
                EditText teamname_edittext = (EditText) findViewById(R.id.team_name);
                EditText teamcode_edittext = (EditText) findViewById(R.id.team_code);
                String teamname = teamname_edittext.getText().toString();
                String teamcode = teamcode_edittext.getText().toString();

               /* JSONObject obj = new JSONObject();
                try {
                    obj.put("username", teamname);
                    obj.put("password",teamcode);
                    Login_Api_Call login_api_call = new Login_Api_Call();
                    login_api_call.execute(obj.toString()).get();

                } catch (JSONException e) {
                    e.printStackTrace();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (ExecutionException e) {
                    e.printStackTrace();
                }*/

                Intent i = new Intent(Login.this, MainActivity.class);
                startActivity(i);
            }
        });
    }

}
