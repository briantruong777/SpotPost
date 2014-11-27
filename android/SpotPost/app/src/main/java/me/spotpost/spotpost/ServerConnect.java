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
}
