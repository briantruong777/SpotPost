package me.spotpost.spotpost;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.util.Log;

/**
 * Maintains the connection to the server
 */
class ServerConnect
{
    private static final String TAG = "ServerConnect";

    private Context context;
    private ConnectivityManager connMgr;
    private MapsActivity mapActivity;

    public ServerConnect(Context context, MapsActivity mapActivity)
    {
        this.context = context;
        connMgr = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
        this.mapActivity = mapActivity;
    }

    /**
     * Logs into website
     *
     * @param username Username to login with
     * @param password Password to login with
     * @return true if successfully started background LoginTask
     */
    public boolean login(String username, String password)
    {
        if (username == null || password == null)
        {
            Log.d(TAG, "username or password was null");
            return false;
        }

        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo == null || !networkInfo.isConnected())
        {
            Log.d(TAG, "no network connection");
            return false;
        }

        (new LoginTask()).execute(username, password);
        return true;
    }
    private class LoginTask extends AsyncTask<String, Void, String>
    {
        @Override
        protected String doInBackground(String... strArr)
        {
            String username = strArr[0];
            String password = strArr[1];

            return null;
        }

        @Override
        protected void onPostExecute(String result)
        {
            mapActivity.onLogin(true);
        }
    }
}
