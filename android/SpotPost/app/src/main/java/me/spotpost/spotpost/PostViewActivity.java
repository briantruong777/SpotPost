package me.spotpost.spotpost;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewTreeObserver;
import android.widget.FrameLayout;
import android.widget.ImageButton;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.JsonHttpResponseHandler;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;


public class PostViewActivity extends Activity
{
    private static final String TAG = "PostViewActivity";

    private View mProgressView;

    private int mPostId;

    private TextView mTitleView;
    private TextView mContentView;
    private TextView mUserView;
    private TextView mRepView;
    private TextView mTimeView;

    private ImageButton mUpButton;
    private ImageButton mDownButton;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_post_view);
        mProgressView = setupProgressBar();

        Intent intent = getIntent();
        mPostId = intent.getIntExtra(MapsActivity.EXTRA_POST_ID, 0);

        mTitleView = (TextView) findViewById(R.id.title);
        mContentView = (TextView) findViewById(R.id.content);
        mUserView = (TextView) findViewById(R.id.user);
        mRepView = (TextView) findViewById(R.id.rep);
        mTimeView = (TextView) findViewById(R.id.time);

        mUpButton = (ImageButton) findViewById(R.id.upvote);
        mUpButton.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                SpotpostClient.upvote(mPostId, new AsyncHttpResponseHandler()
                {
                    @Override
                    public void onSuccess(int i, Header[] headers, byte[] bytes)
                    {
                        Log.d(TAG, "Upvote successful");
                        SpotpostClient.getSpotPost(mPostId, new GetSpotPostHandler());
                    }

                    @Override
                    public void onFailure(int i, Header[] headers, byte[] bytes, Throwable throwable)
                    {
                        Log.d(TAG, "Failed to upvote: " + throwable);
                    }
                });
            }
        });
        mDownButton = (ImageButton) findViewById(R.id.downvote);
        mDownButton.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                SpotpostClient.downvote(mPostId, new AsyncHttpResponseHandler()
                {
                    @Override
                    public void onSuccess(int i, Header[] headers, byte[] bytes)
                    {
                        Log.d(TAG, "Downvote successful");
                        SpotpostClient.getSpotPost(mPostId, new GetSpotPostHandler());
                    }

                    @Override
                    public void onFailure(int i, Header[] headers, byte[] bytes, Throwable throwable)
                    {
                        Log.d(TAG, "Failed to downvote: " + throwable);
                    }

                    @Override
                    public void onStart()
                    {
                        mProgressView.setVisibility(View.VISIBLE);
                    }

                    @Override
                    public void onFinish()
                    {
                        mProgressView.setVisibility(View.INVISIBLE);
                    }
                });
            }
        });

        SpotpostClient.getSpotPost(mPostId, new GetSpotPostHandler());
    }

    private class GetSpotPostHandler extends JsonHttpResponseHandler
    {
        @Override
        public void onSuccess(int statusCode, Header[] headers, JSONArray response)
        {
            try
            {
                Log.d(TAG, "JSON Response:\n" + response.toString(2));
                if (response.length() == 1)
                {
                    JSONObject post = response.getJSONObject(0);
                    mTitleView.setText(post.getString("title"));
                    mContentView.setText(post.getString("content"));
                    mUserView.setText(post.getJSONObject("user").getString("username"));
                    mRepView.setText(post.getString("reputation"));
                    mTimeView.setText(post.getString("time"));
                }
                else
                {
                    Log.d(TAG, "Received incorrect number of SpotPosts");
                }
            }
            catch (JSONException e)
            {
                Log.d(TAG, "JSON Exception: " + e);
                Log.d(TAG, "Couldn't determine login state");
            }
        }

        @Override
        public void onFailure(int statusCode, Header[] headers, String responseString, Throwable error)
        {
            Log.d(TAG, "Get SpotPost HTTP Failure: " + responseString, error);
            Log.d(TAG, "Couldn't get SpotPost");
        }

        @Override
        public void onStart()
        {
            mProgressView.setVisibility(View.VISIBLE);
        }

        @Override
        public void onFinish()
        {
            mProgressView.setVisibility(View.INVISIBLE);
        }
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
}
