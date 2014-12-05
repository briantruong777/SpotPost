package me.spotpost.spotpost;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewTreeObserver;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;
import android.widget.Space;
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

    private boolean mUnlock;

    private TextView mTitleView;
    private TextView mContentView;
    private TextView mUserView;
    private TextView mRepView;
    private TextView mTimeView;

    private ImageButton mUpButton;
    private ImageButton mDownButton;
    private Button mUnlockButton;

    private LinearLayout mCommentLayout;

    private EditText mNewCommentView;
    private Button mNewCommentBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_post_view);
        mProgressView = setupProgressBar();

        Intent intent = getIntent();
        mPostId = intent.getIntExtra(MapsActivity.EXTRA_POST_ID, 0);
        mUnlock = intent.getBooleanExtra(MapsActivity.EXTRA_UNLOCK, false);
        Log.d(TAG, "Unlock: " + mUnlock);

        mTitleView = (TextView) findViewById(R.id.title);
        mContentView = (TextView) findViewById(R.id.content);
        mUserView = (TextView) findViewById(R.id.user);
        mRepView = (TextView) findViewById(R.id.rep);
        mTimeView = (TextView) findViewById(R.id.time);

        mUpButton = (ImageButton) findViewById(R.id.upvote);
        mUpButton.setEnabled(false);
        mUpButton.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                SpotpostClient.upvoteSpotPost(mPostId, new AsyncHttpResponseHandler()
                {
                    @Override
                    public void onSuccess(int i, Header[] headers, byte[] bytes)
                    {
                        Log.d(TAG, "Upvote successful");
                        SpotpostClient.getSpotPost(mPostId, 2, new GetSpotPostHandler());
                    }

                    @Override
                    public void onFailure(int i, Header[] headers, byte[] bytes, Throwable throwable)
                    {
                        Log.d(TAG, "Failed to upvote: " + throwable);
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
        mDownButton = (ImageButton) findViewById(R.id.downvote);
        mDownButton.setEnabled(false);
        mDownButton.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                SpotpostClient.downvoteSpotPost(mPostId, new AsyncHttpResponseHandler()
                {
                    @Override
                    public void onSuccess(int i, Header[] headers, byte[] bytes)
                    {
                        Log.d(TAG, "Downvote successful");
                        SpotpostClient.getSpotPost(mPostId, 2, new GetSpotPostHandler());
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

        mUnlockButton = (Button) findViewById(R.id.unlock_btn);
        mUnlockButton.setEnabled(false);
        mUnlockButton.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                SpotpostClient.unlockSpotPost(mPostId, new UnlockHandler());
            }
        });

        mCommentLayout = (LinearLayout) findViewById(R.id.comment_layout);

        mNewCommentView = (EditText) findViewById(R.id.new_comment_view);
        mNewCommentView.setEnabled(false);
        mNewCommentBtn = (Button) findViewById(R.id.new_comment_btn);
        mNewCommentBtn.setEnabled(false);
        mNewCommentBtn.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                String content = mNewCommentView.getText().toString();
                if (content.length() > 0)
                {
                    SpotpostClient.postComment(mPostId, content, new JsonHttpResponseHandler()
                    {
                        @Override
                        public void onSuccess(int statusCode, Header[] headers, JSONObject response)
                        {
                            try
                            {
                                Log.d(TAG, "Received JSON:\n" + response.toString(2));
                                if (response.getInt("code") == 1000)
                                {
                                    Log.d(TAG, "Comment post was successful");
                                    mNewCommentView.setText("");
                                    SpotpostClient.getSpotPost(mPostId, 2, new GetSpotPostHandler());
                                }
                                else
                                {
                                    Log.d(TAG, "Unable to post comment");
                                }
                            }
                            catch (JSONException e)
                            {
                                Log.d(TAG, "JSON Exception: " + e);
                            }
                        }

                        @Override
                        public void onFailure(int statusCode, Header[] headers, String responseString, Throwable error)
                        {
                            Log.d(TAG, "Get SpotPost HTTP Failure: " + responseString, error);
                            Log.d(TAG, "Couldn't post comment");
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
            }
        });

        if (mUnlock)
        {
            SpotpostClient.unlockSpotPost(mPostId, new UnlockHandler());
        }
        else
        {
            SpotpostClient.getSpotPost(mPostId, 2, new GetSpotPostHandler());
        }
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
                    setupViews(response);
                }
                else if (response.length() == 0)
                {
                    mTitleView.setText("LOCKED");
                    mContentView.setText("LOCKED");
                    mUserView.setText("LOCKED");
                    mRepView.setText("LOCKED");
                    mTimeView.setText("LOCKED");

                    mUnlockButton.setEnabled(true);
                }
                else
                {
                    Log.d(TAG, "Received incorrect number of SpotPosts");
                }
            }
            catch (JSONException e)
            {
                Log.d(TAG, "JSON Exception: " + e);
                Log.d(TAG, "Couldn't get Spotpost");
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

    private class UnlockHandler extends JsonHttpResponseHandler
    {
        @Override
        public void onSuccess(int statusCode, Header[] headers, JSONArray response)
        {
            try
            {
                Log.d(TAG, "JSON Response:\n" + response.toString(2));
                if (response.length() == 1)
                {
                    setupViews(response);

                    mUnlockButton.setEnabled(false);
                }
                else
                {
                    Log.d(TAG, "Received incorrect number of SpotPosts");
                }
            }
            catch (JSONException e)
            {
                Log.d(TAG, "JSON Exception: " + e);
            }
        }

        @Override
        public void onFailure(int statusCode, Header[] headers, String responseString, Throwable error)
        {
            Log.d(TAG, "Unlock SpotPost HTTP Failure: " + responseString, error);
            Log.d(TAG, "Couldn't unlock SpotPost");
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

    private void setupViews(JSONArray response) throws JSONException
    {
        JSONObject post = response.getJSONObject(0);
        mTitleView.setText(post.getString("title"));
        mContentView.setText(post.getString("content"));
        mUserView.setText(post.getJSONObject("user").getString("username"));
        mRepView.setText(post.getString("reputation"));
        mTimeView.setText(post.getString("time"));
        mUpButton.setEnabled(true);
        mDownButton.setEnabled(true);

        mNewCommentView.setEnabled(true);
        mNewCommentBtn.setEnabled(true);

        mCommentLayout.removeAllViews();
        JSONArray comments = post.getJSONArray("comments");
        for (int i = 0; i < comments.length(); i++)
        {
            JSONObject comment = comments.getJSONObject(i);
            String content = comment.getString("content");
            String username = comment.getString("username");
            String rep = comment.getString("reputation");
            String time =  comment.getString("time");
            mCommentLayout.addView(new CommentView(PostViewActivity.this, content, username, rep, time, comment.getInt("id")));
        }
    }

    private class CommentView extends LinearLayout
    {
        int commentId;

        public CommentView(Context context, String content, String username, String rep, String time, int id)
        {
            super(context);
            commentId = id;

            setOrientation(HORIZONTAL);
            setLayoutParams(new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

            ImageButton upvoteBtn = new ImageButton(context);
            upvoteBtn.setOnClickListener(new CommentUpvoteListener());
            upvoteBtn.setImageResource(R.drawable.ic_action_collapse);
            upvoteBtn.setLayoutParams(new ViewGroup.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

            TextView repView = new TextView(context);
            repView.setText(rep);
            repView.setLayoutParams(new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
            repView.setGravity(Gravity.CENTER);

            ImageButton downvoteBtn = new ImageButton(context);
            downvoteBtn.setOnClickListener(new CommentDownvoteListener());
            downvoteBtn.setImageResource(R.drawable.ic_action_expand);
            downvoteBtn.setLayoutParams(new ViewGroup.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

            LinearLayout voteLayout = new LinearLayout(context);
            voteLayout.setLayoutParams(new ViewGroup.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
            voteLayout.setOrientation(VERTICAL);
            voteLayout.addView(upvoteBtn);
            voteLayout.addView(repView);
            voteLayout.addView(downvoteBtn);

            Space spaceView = new Space(context);
            spaceView.setLayoutParams(new ViewGroup.LayoutParams(100, ViewGroup.LayoutParams.MATCH_PARENT));

            LinearLayout contentLayout = new LinearLayout(context);
            contentLayout.setLayoutParams(new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
            contentLayout.setGravity(Gravity.CENTER_VERTICAL);
            contentLayout.setOrientation(VERTICAL);

            TextView contentView = new TextView(context);
            contentView.setText(content);
            contentView.setTextSize(TypedValue.COMPLEX_UNIT_SP, 20);

            TextView extraView = new TextView(context);
            extraView.setText("by " + username + "\nat " + time);
            extraView.setTextColor(0xffcccccc);

            contentLayout.addView(contentView);
            contentLayout.addView(extraView);

            addView(voteLayout);
            addView(spaceView);
            addView(contentLayout);
        }

        private class CommentUpvoteListener implements View.OnClickListener
        {
            @Override
            public void onClick(View v)
            {
                Log.d(TAG, "Comment Upvote id: " + commentId);
                SpotpostClient.upvoteComment(commentId, new AsyncHttpResponseHandler()
                {
                    @Override
                    public void onSuccess(int status, Header[] headers, byte[] bytes)
                    {
                        Log.d(TAG, "Success upvoting comment");
                        SpotpostClient.getSpotPost(mPostId, 2, new GetSpotPostHandler());
                    }

                    @Override
                    public void onFailure(int status, Header[] headers, byte[] bytes, Throwable throwable)
                    {
                        Log.d(TAG, "Failure upvoting comment: " + status + " " + throwable);
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
        }
        private class CommentDownvoteListener implements View.OnClickListener
        {
            @Override
            public void onClick(View v)
            {
                Log.d(TAG, "Comment Downvote id: " + commentId);
                SpotpostClient.downvoteComment(commentId, new AsyncHttpResponseHandler()
                {
                    @Override
                    public void onSuccess(int status, Header[] headers, byte[] bytes)
                    {
                        Log.d(TAG, "Success downvoting comment");
                        SpotpostClient.getSpotPost(mPostId, 2, new GetSpotPostHandler());
                    }

                    @Override
                    public void onFailure(int status, Header[] headers, byte[] bytes, Throwable throwable)
                    {
                        Log.d(TAG, "Failure downvoting comment: " + status + " " + throwable);
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
