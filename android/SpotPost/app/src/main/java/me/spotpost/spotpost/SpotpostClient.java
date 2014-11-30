package me.spotpost.spotpost;

import android.content.Context;
import android.util.Log;

import org.apache.http.HttpEntity;
import org.apache.http.entity.StringEntity;
import org.json.JSONException;
import org.json.JSONObject;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.PersistentCookieStore;
import com.loopj.android.http.RequestParams;
import com.loopj.android.http.SyncHttpClient;

import java.io.UnsupportedEncodingException;

/**
 * Static class that encapsulates usage of SpotPost API
 */
public class SpotpostClient
{
    private static final String TAG = "SpotpostClient";
    private static final String JSON_APP = "application/json";
    private static final String BASE_URL = "http://spotpost.me/";

    private static Context context = null;
    private static AsyncHttpClient client = new AsyncHttpClient();
    private static SyncHttpClient synClient = new SyncHttpClient();
    private static PersistentCookieStore cookieStore = null;

    /**
     * Sets up this static class. Should be called between switching of activities (I think).
     */
    public static void setup(Context pContext)
    {
        context = pContext;
        cookieStore = new PersistentCookieStore(context);
        client.setCookieStore(cookieStore);
    }


    /**
     * Returns true if logged in currently.
     */
    public static void isLoggedIn(AsyncHttpResponseHandler handler)
    {
        get("_userstatus", null, handler);
    }

    /**
     * Login with given username and password
     */
    public static void login(String username, String password, AsyncHttpResponseHandler handler)
    {
        JSONObject json = new JSONObject();
        try
        {
            json.put("username", username);
            json.put("password", password);
        }
        catch (JSONException e)
        {
            Log.d(TAG, "Unable to construct JSON: " + e);
            return;
        }

        StringEntity entity = null;
        try
        {
            entity = new StringEntity(json.toString());
        }
        catch (UnsupportedEncodingException e)
        {
            Log.d(TAG, "Unable to create StringEntity: " + e);
        }

        post("login", entity, JSON_APP, handler);
    }

    /**
     * Makes a generic get request with given parameters
     */
    public static void get(String url, RequestParams params, AsyncHttpResponseHandler handler)
    {
        client.get(BASE_URL+url, params, handler);
    }
    /**
     * Makes a synchronous get request
     */
    public static void synGet(String url, RequestParams params, AsyncHttpResponseHandler handler)
    {
        synClient.get(BASE_URL+url, params, handler);
    }
    /**
     * Makes a generic post request with given parameters
     */
    public static void post(String url, HttpEntity entity, String contentType, AsyncHttpResponseHandler handler)
    {
        client.post(context, BASE_URL+url, entity, contentType, handler);
    }
}
