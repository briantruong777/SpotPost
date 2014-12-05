package me.spotpost.spotpost;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Build;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.view.ViewTreeObserver;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.ProgressBar;

import com.loopj.android.http.JsonHttpResponseHandler;

import org.apache.http.Header;
import org.json.JSONException;
import org.json.JSONObject;


public class PostActivity extends Activity
{
    private static final String TAG = "PostActivity";

    private View mProgressView;
    private EditText mTitleView;
    private EditText mContentView;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_post);

        mTitleView = (EditText) findViewById(R.id.title);
        mContentView = (EditText) findViewById(R.id.content);

        Button mPostButton = (Button) findViewById(R.id.post_button);
        mPostButton.setOnClickListener(new OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                attemptPost();
            }
        });

        mProgressView = setupProgressBar();
    }

    private View setupProgressBar()
    {
        // create new ProgressBar and style it
        final ProgressBar progressBar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progressBar.setLayoutParams(new ActionBar.LayoutParams(ActionBar.LayoutParams.MATCH_PARENT, 36));
        progressBar.setIndeterminate(true);
        progressBar.setVisibility(View.INVISIBLE);

        // retrieve the top view of our application
        final FrameLayout decorView = (FrameLayout) getWindow().getDecorView();
        decorView.addView(progressBar);

        // Here we try to position the ProgressBar to the correct position by looking
        // at the position where content area starts. But during creating time, sizes
        // of the components are not set yet, so we have to wait until the components
        // has been laid out
        // Also note that doing progressBar.setY(136) will not work, because of different
        // screen densities and different sizes of actionBar
        ViewTreeObserver observer = progressBar.getViewTreeObserver();
        observer.addOnGlobalLayoutListener(new ViewTreeObserver.OnGlobalLayoutListener() {
            @Override
            public void onGlobalLayout() {
                View contentView = decorView.findViewById(android.R.id.content);
                progressBar.setY(contentView.getY() - 25);

                ViewTreeObserver observer = progressBar.getViewTreeObserver();
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN)
                    observer.removeOnGlobalLayoutListener(this);
                else
                    observer.removeGlobalOnLayoutListener(this);
            }
        });

        return progressBar;
    }

    private void attemptPost()
    {
        // Reset errors.
        mTitleView.setError(null);
        mContentView.setError(null);

        String title = mTitleView.getText().toString();
        String content = mContentView.getText().toString();

        boolean cancel = false;
        View focusView = null;

        if (TextUtils.isEmpty(title))
        {
            mTitleView.setError(getString(R.string.error_field_required));
            focusView = mTitleView;
            cancel = true;
        }

        if (TextUtils.isEmpty(content))
        {
            mContentView.setError(getString(R.string.error_field_required));
            focusView = mContentView;
            cancel = true;
        }

        if (cancel)
        {
            // There was an error; don't attempt login and focus the first
            // form field with an error.
            focusView.requestFocus();
        }
        else
        {
            ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
            NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
            if (networkInfo != null && networkInfo.isConnected())
            {
                Intent intent = getIntent();
                double lat = intent.getDoubleExtra(MapsActivity.EXTRA_LATITUDE, 0);
                double lng = intent.getDoubleExtra(MapsActivity.EXTRA_LONGITUDE, 0);
                SpotpostClient.postSpotPosts(title, content, lat, lng, new JsonHttpResponseHandler()
                {
                    @Override
                    public void onSuccess(int statusCode, Header[] headers, JSONObject response)
                    {
                        try
                        {
                            Log.d(TAG, "JSON Response: " + response.toString(2));
                            if (response.getJSONObject("error").getInt("code") == 1000)
                            {
                                Log.d(TAG, "Successfully made SpotPost!");
                                finish();
                            }
                            else
                            {
                                Log.d(TAG, "Unable to post Spotpost");
                            }
                        }
                        catch (JSONException e)
                        {
                            Log.d(TAG, "Received invalid JSON: " + e);
                        }
                    }

                    @Override
                    public void onFailure(int statusCode, Header[] headers, String responseString, Throwable error)
                    {
                        Log.d(TAG, "Post HTTP Failure: " + responseString, error);
                    }

                    @Override
                    public void onStart()
                    {
                        showProgress(true);
                    }
                    @Override
                    public void onFinish()
                    {
                        showProgress(false);
                    }
                });
            }
            else
            {
                //TODO Say more about this
                Log.d(TAG, "network is not active");
            }
        }
    }

    /**
     * Shows the progress UI and hides the login form.
     */
    public void showProgress(final boolean show)
    {
        int shortAnimTime = getResources().getInteger(android.R.integer.config_shortAnimTime);

        mProgressView.setVisibility(show ? View.VISIBLE : View.INVISIBLE);
    }
}
