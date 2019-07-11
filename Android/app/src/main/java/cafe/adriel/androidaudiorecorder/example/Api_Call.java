package cafe.adriel.androidaudiorecorder.example;

import android.os.AsyncTask;
        import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
        import java.io.BufferedWriter;
        import java.io.IOException;
        import java.io.InputStream;
        import java.io.InputStreamReader;
        import java.io.OutputStreamWriter;
        import java.io.Writer;
        import java.net.HttpURLConnection;
        import java.net.URL;

public class Api_Call extends AsyncTask<String,String,String >
{
    protected String doInBackground(String... params) {
        String JsonResponse = null;
        String JsonDATA = params[0];
        HttpURLConnection urlConnection = null;
        BufferedReader reader = null;
        String TAG="My_tag";
        try {
            String ibm ="http://demointernhack2019.mybluemix.net/recording/";
            //String temp = "https://tnp-app.herokuapp.com/app_notify/";
            URL url = new URL(ibm);
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setDoOutput(true);

            //set headers and method
            urlConnection.setRequestMethod("POST");
            urlConnection.setRequestProperty("Content-Type", "application/json");
            urlConnection.setRequestProperty("Accept", "application/json");

            // is output buffer writter
            Writer writer = new BufferedWriter(new OutputStreamWriter(urlConnection.getOutputStream(), "UTF-8"));
            writer.write(JsonDATA);

            writer.close();

            //input stream
            InputStream inputStream = urlConnection.getInputStream();
            Log.e("urlError",inputStream.toString());

            StringBuffer buffer = new StringBuffer();
            if (inputStream == null) {
                // Nothing to do.
                return null;
            }
            reader = new BufferedReader(new InputStreamReader(inputStream));


            String inputLine;
            while ((inputLine = reader.readLine()) != null)
                buffer.append(inputLine + "\n");

            buffer.deleteCharAt(buffer.length()-1);

            if (buffer.length() == 0) {
                // Stream was empty. No point in parsing.
                return null;
            }

            //response data
            JsonResponse = buffer.toString();
            Log.e("response",JsonResponse);

            try {
                //send to post execute
                return JsonResponse;
            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;

        } catch (IOException e)
        {
            e.printStackTrace();
        }  finally {
            if (urlConnection != null) {
                urlConnection.disconnect();
            }
            if (reader != null) {
                try {
                    reader.close();
                } catch (final IOException e) {
                    Log.e(TAG, "Error closing stream", e);
                }
            }
        }
        return null;
    }


    @Override
    protected void onPreExecute() {
        // TODO Auto-generated method stub

        super.onPreExecute();

    }


    @Override
    protected void onPostExecute(String args) {
        // TODO Auto-generated method stub


    }
}
