package cafe.adriel.androidaudiorecorder.example;

import android.Manifest;
import android.content.Intent;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.os.Environment;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Toast;

import org.json.JSONObject;

import cafe.adriel.androidaudiorecorder.AndroidAudioRecorder;
import cafe.adriel.androidaudiorecorder.model.AudioChannel;
import cafe.adriel.androidaudiorecorder.model.AudioSampleRate;
import cafe.adriel.androidaudiorecorder.model.AudioSource;

import java.io.DataInputStream;
import java.io.FileInputStream;
import java.util.Calendar;
import java.util.Date;
import java.text.SimpleDateFormat;
import java.io.InputStream;
import java.io.ByteArrayOutputStream;
import java.io.BufferedInputStream;
import android.util.Base64;
import java.io.File;
//import com.ibm.cloud.sdk.core.service.security.IamOptions;
//import com.ibm.watson.speech_to_text.v1.SpeechToText;

public class MainActivity extends AppCompatActivity {
    private static final int REQUEST_RECORD_AUDIO = 0;
    private static final SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd_HHmmss");
    private static final String currentDateandTime = sdf.format(new Date());
    String FILENAME=currentDateandTime;
    private static final String AUDIO_FILE_PATH =
            Environment.getExternalStorageDirectory().getPath() + "/"+currentDateandTime+"_transcript.wav";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setBackgroundDrawable(
                    new ColorDrawable(ContextCompat.getColor(this, R.color.colorPrimaryDark)));
        }

        Util.requestPermission(this, Manifest.permission.RECORD_AUDIO);
        Util.requestPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_RECORD_AUDIO) {
            if (resultCode == RESULT_OK) {
                /*IamOptions options = new IamOptions.Builder()
                        .apiKey("9e0ri-mtT_R8DicTjLTNkRe9T1WJFxHdkFBYobAmlxp2")
                        .build();
                SpeechToText speechToText = new SpeechToText(options);
                speechToText.setEndPoint("https://gateway-wdc.watsonplatform.net/speech-to-text/api");*/
                //Toast.makeText(this,AUDIO_FILE_PATH,Toast.LENGTH_LONG).show();
                Toast.makeText(this, "Audio recorded successfully!", Toast.LENGTH_SHORT).show();
//                call rest api

                JSONObject obj = new JSONObject();
                try {
//                    obj.put("name", "pooja");
//                    Api_Call api_call = new Api_Call();
//                    api_call.execute(obj.toString()).get();
                    int read;
                    File file = new File(AUDIO_FILE_PATH);
                    InputStream inStream = new DataInputStream(new FileInputStream(file));
                    ByteArrayOutputStream out = new ByteArrayOutputStream();
                    BufferedInputStream in = new BufferedInputStream(inStream);

                    byte[] buff = new byte[1024];
                    while ((read = in.read(buff)) > 0) {
                        out.write(buff, 0, read);
                    }
                    out.flush();
                    byte[] fileAudioByte = out.toByteArray();

                    String encodedString = Base64.encodeToString(fileAudioByte, Base64.DEFAULT);
                    obj.put("file_name", "transcript");
                    obj.put("file_data",encodedString);
                    Api_Call api_call = new Api_Call();
                    api_call.execute(obj.toString()).get();


                }
                catch (Exception e){
                    e.printStackTrace();
                }
            } else if (resultCode == RESULT_CANCELED) {
                Toast.makeText(this, "Audio was not recorded", Toast.LENGTH_SHORT).show();
            }
        }
    }

    public void recordAudio(View v) {
        AndroidAudioRecorder.with(this)
                // Required
                .setFilePath(AUDIO_FILE_PATH)
                .setColor(ContextCompat.getColor(this, R.color.recorder_bg))
                .setRequestCode(REQUEST_RECORD_AUDIO)

                // Optional
                .setSource(AudioSource.MIC)
                .setChannel(AudioChannel.STEREO)
                .setSampleRate(AudioSampleRate.HZ_48000)
                .setAutoStart(false)
                .setKeepDisplayOn(true)

                // Start recording
                .record();
        System.out.print(Environment.getExternalStorageDirectory().getPath());
    }

}