package me.spotpost.spotpost;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Build;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewTreeObserver;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.util.Log;

import com.loopj.android.http.JsonHttpResponseHandler;

import org.apache.http.Header;
import org.json.JSONException;
import org.json.JSONObject;


/**
 * A login screen that offers login via username/password.
 */
public class LoginActivity extends Activity
{
    private static final String TAG = "LoginActivity";

    private EditText mUsernameView;
    private EditText mPasswordView;
    private View mProgressView;
    private View mLoginFormView;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        mUsernameView = (EditText) findViewById(R.id.username);

        mPasswordView = (EditText) findViewById(R.id.password);
        mPasswordView.setOnEditorActionListener(new TextView.OnEditorActionListener()
        {
            @Override
            public boolean onEditorAction(TextView textView, int id, KeyEvent keyEvent)
            {
                if (id == R.id.login || id == EditorInfo.IME_NULL)
                {
                    attemptLogin();
                    return true;
                }
                return false;
            }
        });

        Button mUsernameSignInButton = (Button) findViewById(R.id.username_sign_in_button);
        mUsernameSignInButton.setOnClickListener(new OnClickListener()
        {
            @Override
            public void onClick(View view)
            {
                attemptLogin();
            }
        });

        mLoginFormView = findViewById(R.id.login_form);

        setupProgressBar();
    }

    /**
     * Sets up progress bar
     */
    private void setupProgressBar()
    {
        // create new ProgressBar and style it
        final ProgressBar progressBar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progressBar.setLayoutParams(new ActionBar.LayoutParams(ActionBar.LayoutParams.MATCH_PARENT, 36));
        progressBar.setIndeterminate(true);
        progressBar.setVisibility(View.INVISIBLE);
        mProgressView = progressBar;

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
    }

    /**
     * Attempts to sign in or register the account specified by the login form.
     * If there are form errors (invalid email, missing fields, etc.), the
     * errors are presented and no actual login attempt is made.
     */
    public void attemptLogin()
    {
        // Reset errors.
        mUsernameView.setError(null);
        mPasswordView.setError(null);

        // Store values at the time of the login attempt.
        String email = mUsernameView.getText().toString();
        String password = mPasswordView.getText().toString();

        boolean cancel = false;
        View focusView = null;

        // Check for a valid email address.
        if (TextUtils.isEmpty(email))
        {
            mUsernameView.setError(getString(R.string.error_field_required));
            focusView = mUsernameView;
            cancel = true;
        }

        // Check for a valid password, if the user entered one.
        if (TextUtils.isEmpty(password))
        {
            mPasswordView.setError(getString(R.string.error_invalid_password));
            focusView = mPasswordView;
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
                SpotpostClient.login(email, password, new JsonHttpResponseHandler()
                {
                    @Override
                    public void onStart()
                    {
                        showProgress(true);
                    }

                    @Override
                    public void onSuccess(int statusCode, Header[] headers, JSONObject response)
                    {
                        try
                        {
                            Log.d(TAG, "JSON Response: " + response.toString(2));

                            if (response.getInt("code") == 1000)
                            {
                                // Success logging in
                                finish();
                            }
                            else
                            {
                                Log.d(TAG, "Failed to login");
                                mPasswordView.setError(getString(R.string.error_invalid_password));
                            }
                        }
                        catch (JSONException e)
                        {
                            Log.d(TAG, "Recieved invalid JSON: " + e);
                        }
                    }

                    @Override
                    public void onFailure(int statusCode, Header[] headers, String responseString, Throwable error)
                    {
                        Log.d(TAG, "Login HTTP Failure: " + responseString, error);
                        mPasswordView.setError(getString(R.string.error_invalid_password));
                    }

                    @Override
                    public void onFinish ()
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



