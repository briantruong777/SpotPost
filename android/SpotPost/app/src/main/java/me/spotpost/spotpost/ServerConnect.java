package me.spotpost.spotpost;

import android.content.Context;
import android.net.ConnectivityManager;
import android.os.AsyncTask;

/**
 * Maintains the connection to the server
 */
class ServerConnect
{
    String username;
    String password;

    Context context;
    ConnectivityManager connMgr;
    MapsActivity mapActivity;

    public ServerConnect(Context context, MapsActivity mapActivity)
    {
        username = null;
        password = null;

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
            return false;

        return true;
    }
    private class LoginTask extends AsyncTask<Void, Void, String>
    {
        @Override
        protected String doInBackground(Void... blah)
        {
            return null;
        }

        @Override
        protected void onPostExecute(String result)
        {
            mapActivity.onLogin(true);
        }
    }

    /**
     * Logs out of website
     *
     * @return true if successfully started background LoginTask
     */
    public boolean logout()
    {
        return true;
    }

    private class LogoutTask extends AsyncTask<Void, Void, String>
    {
        @Override
        protected String doInBackground(Void... blah)
        {
            return null;
        }

        @Override
        protected void onPostExecute(String result)
        {
            mapActivity.onLogout(true);
        }
    }
}
