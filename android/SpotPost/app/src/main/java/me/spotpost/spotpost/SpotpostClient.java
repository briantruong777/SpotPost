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
     * Sets up this static class. Should probably be called once during lifetime of app.
     */
    public static void setup(Context pContext)
    {
        context = pContext;
        cookieStore = new PersistentCookieStore(context);
        client.setCookieStore(cookieStore);
    }


    /**
     * Checks if logged in already or not
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

    public static void logout(AsyncHttpResponseHandler handler)
    {
        get("_logout", null, handler);
    }

    /**
     * Get nearby spotposts
     */
    public static void getSpotPostsHere(double lat, double lng, AsyncHttpResponseHandler handler)
    {
        RequestParams params = new RequestParams();
        params.put("latitude", lat);
        params.put("longitude", lng);
        params.put("radius", 10000.0);
        Log.d(TAG, "params: " + params.toString());
        get("spotpost/_getlocation", params, handler);
    }

    public static void getSpotPost(int id, int lockValue, AsyncHttpResponseHandler handler)
    {
        RequestParams params = new RequestParams();
        params.put("id", id);
        params.put("lock_value", lockValue);
        Log.d(TAG, "Getting SpotPost id: " + id);
        get("spotpost/_get", params, handler);
    }

    public static void unlockSpotPost(int id, AsyncHttpResponseHandler handler)
    {
        RequestParams params = new RequestParams();
        params.put("id", id);
        params.put("unlock_posts", 1);
        Log.d(TAG, "Unlocking SpotPost id: " + id);
        get("spotpost/_get", params, handler);
    }

    /**
     * Post a SpotPost
     */
    public static void postSpotPosts(String title, String content, double lat, double lng, AsyncHttpResponseHandler handler)
    {
        JSONObject json = new JSONObject();
        try
        {
            json.put("title", title);
            json.put("content", content);
            json.put("latitude", lat);
            json.put("longitude", lng);
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
            Log.d(TAG, "Posting:\n" + json.toString(2));
        }
        catch (UnsupportedEncodingException e)
        {
            Log.d(TAG, "Unable to create StringEntity: " + e);
        }
        catch (JSONException e)
        {
            Log.d(TAG, "JSON Exception: " + e);
        }

        post("spotpost/_post", entity, JSON_APP, handler);
    }

    public static void upvoteSpotPost(int postId, AsyncHttpResponseHandler handler)
    {
        get("spotpost/_upvote/"+postId, null, handler);
    }
    public static void downvoteSpotPost(int postId, AsyncHttpResponseHandler handler)
    {
        get("spotpost/_downvote/"+postId, null, handler);
    }

    public static void postComment(int postId, String content, AsyncHttpResponseHandler handler)
    {
        JSONObject json = new JSONObject();
        try
        {
            json.put("message_id", postId);
            json.put("content", content);
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

        post("comment/_post", entity, JSON_APP, handler);
    }

    public static void upvoteComment(int commentId, AsyncHttpResponseHandler handler)
    {
        get("comment/_upvote/"+commentId, null, handler);
    }
    public static void downvoteComment(int commentId, AsyncHttpResponseHandler handler)
    {
        get("comment/_downvote/"+commentId, null, handler);
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
