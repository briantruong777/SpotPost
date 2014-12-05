package me.spotpost.spotpost;

import android.app.ActionBar;
import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.location.LocationProvider;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewTreeObserver;
import android.widget.FrameLayout;
import android.widget.ProgressBar;

import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.JsonHttpResponseHandler;

import org.apache.http.Header;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class MapsActivity extends FragmentActivity
{
    public static final String EXTRA_LATITUDE = "me.spotpost.spotpost.LATITUDE";
    public static final String EXTRA_LONGITUDE = "me.spotpost.spotpost.LONGITUDE";
    public static final String EXTRA_POST_ID = "me.spotpost.spotpost.POST_ID";

    private static final String TAG = "MapsActivity";

    private GoogleMap mMap; // Might be null if Google Play services APK is not available.
    private HashMap<String, Integer> mMarkerToPostId;
    private View mProgressView;
    private LocationManager mLocManage;
    private LocationListener mLocListen;
    private double mLat;
    private double mLng;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);

        setUpMapIfNeeded();
        mMarkerToPostId = new HashMap<String, Integer>();
        mProgressView = setupProgressBar();
        mLocManage = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        setupMapLoc();
        mLocListen = setupLocListen();
        SpotpostClient.setup(this);
    }

    /**
     * Sets up the map if it is possible to do so (i.e., the Google Play services APK is correctly
     * installed) and the map has not already been instantiated.. This will ensure that we only ever
     * call {@link #setUpMap()} once when {@link #mMap} is not null.
     * <p/>
     * If it isn't installed {@link SupportMapFragment} (and
     * {@link com.google.android.gms.maps.MapView MapView}) will show a prompt for the user to
     * install/update the Google Play services APK on their device.
     * <p/>
     * A user can return to this FragmentActivity after following the prompt and correctly
     * installing/updating/enabling the Google Play services. Since the FragmentActivity may not
     * have been completely destroyed during this process (it is likely that it would only be
     * stopped or paused), {@link #onCreate(Bundle)} may not be called again so we should call this
     * method in {@link #onResume()} to guarantee that it will be called.
     */
    private void setUpMapIfNeeded()
    {
        // Do a null check to confirm that we have not already instantiated the map.
        if (mMap == null)
        {
            // Try to obtain the map from the SupportMapFragment.
            mMap = ((SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map))
                    .getMap();
            // Check if we were successful in obtaining the map.
            if (mMap != null)
            {
                setUpMap();
            }
        }
    }

    /**
     * This is where we can add markers or lines, add listeners or move the camera. In this case, we
     * just add a marker near Africa.
     * <p/>
     * This should only be called once and when we are sure that {@link #mMap} is not null.
     */
    private void setUpMap()
    {
        mMap.addMarker(new MarkerOptions().position(new LatLng(0, 0)).title("Marker"));
        mMap.setMyLocationEnabled(true);
        mMap.setOnInfoWindowClickListener(new GoogleMap.OnInfoWindowClickListener()
        {
            @Override
            public void onInfoWindowClick(Marker marker)
            {
                Intent intent = new Intent(MapsActivity.this, PostViewActivity.class);
                intent.putExtra(EXTRA_POST_ID, mMarkerToPostId.get(marker.getId()));
                MapsActivity.this.startActivity(intent);
            }
        });
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

    private void setupMapLoc()
    {
        Location loc = mLocManage.getLastKnownLocation(LocationManager.GPS_PROVIDER);
        mLat = loc.getLatitude();
        mLng = loc.getLongitude();
        LatLng latLng = new LatLng(mLat, mLng);
        Log.d(TAG, "Init location: " + latLng);
        CameraUpdate camUpdate = CameraUpdateFactory.newLatLngZoom(latLng, 16.0f);
        mMap.moveCamera(camUpdate);
    }

    private LocationListener setupLocListen()
    {
        return new LocationListener()
        {
            @Override
            public void onLocationChanged(Location location)
            {
                mLat = location.getLatitude();
                mLng = location.getLongitude();
            }

            @Override
            public void onStatusChanged(String provider, int status, Bundle extras)
            {
                String mes = "LocationProvider reports status: ";
                switch (status)
                {
                    case LocationProvider.AVAILABLE:
                        mes += "available";
                        break;
                    case LocationProvider.TEMPORARILY_UNAVAILABLE:
                        mes += "temporarily unavailable";
                        break;
                    case LocationProvider.OUT_OF_SERVICE:
                        mes += "out of service";
                        break;
                }
                Log.d(TAG, mes);
            }

            @Override
            public void onProviderEnabled(String provider)
            {
                Log.d(TAG, "LocationProvider enabled");
            }

            @Override
            public void onProviderDisabled(String provider)
            {
                Log.d(TAG, "LocationProvider disabled");
            }
        };
    }

    @Override
    protected void onStart()
    {
        super.onStart();
        setUpMapIfNeeded();
        mLocManage.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000, 0, mLocListen);
        SpotpostClient.isLoggedIn(new LoginHandler());
        getSpotPosts();
    }

    private class LoginHandler extends JsonHttpResponseHandler
    {
        @Override
        public void onStart()
        {
            mProgressView.setVisibility(View.VISIBLE);
        }

        @Override
        public void onSuccess(int statusCode, Header[] headers, JSONObject response)
        {
            try
            {
                Log.d(TAG, "JSON Response:\n" + response.toString(2));

                if (response.getJSONObject("error").getInt("code") != 1000)
                {
                    Intent intent = new Intent(MapsActivity.this, LoginActivity.class);
                    MapsActivity.this.startActivity(intent);
                } else
                {
                    Log.d(TAG, "User is already logged in");
                }
            } catch (JSONException e)
            {
                Log.d(TAG, "JSON Exception: " + e);
                Log.d(TAG, "Couldn't determine login state");
            }
        }

        @Override
        public void onFailure(int statusCode, Header[] headers, String responseString, Throwable error)
        {
            Log.d(TAG, "Login Check HTTP Failure: " + responseString, error);
            Log.d(TAG, "Couldn't determine login state");
        }

        @Override
        public void onFinish()
        {
            mProgressView.setVisibility(View.INVISIBLE);
        }
    }

    private void getSpotPosts()
    {
        Log.d(TAG, "Getting SpotPosts");
        SpotpostClient.getSpotPostsHere(mLat, mLng, new JsonHttpResponseHandler()
        {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONArray response)
            {
                try
                {
                    Log.d(TAG, "Received SpotPost JSON:\n" + response.toString(2));
                    putSpotPostsOnMap(response);
                } catch (JSONException e)
                {
                    Log.d(TAG, "JSON Exception: " + e);
                    Log.d(TAG, "Couldn't get SpotPosts");
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, Throwable error, JSONObject obj)
            {
                Log.d(TAG, "Get SpotPosts HTTP Failure: " + statusCode, error);
                try
                {
                    if (obj != null)
                        Log.d(TAG, "JSON Object Received:\n" + obj.toString(2));
                } catch (JSONException e)
                {
                    Log.d(TAG, "JSON Exception " + e);
                }
                Log.d(TAG, "Couldn't get SpotPosts");
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, String responseString, Throwable error)
            {
                Log.d(TAG, "Get SpotPosts HTTP Failure: " + responseString, error);
                Log.d(TAG, "Couldn't get SpotPosts");
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

    private void putSpotPostsOnMap(JSONArray spotPosts)
    {
        Log.d(TAG, "Putting posts on map");
        mMap.clear();
        mMarkerToPostId.clear();
        try
        {
            for (int i = 0; i < spotPosts.length(); i++)
            {
                JSONObject post = spotPosts.getJSONObject(i);
                LatLng latLng = new LatLng(post.getDouble("latitude"), post.getDouble("longitude"));
                String title = post.getString("title");
                String content = post.getJSONObject("user").getString("username");
                content += " at " + post.getString("time");

                Marker marker = mMap.addMarker(new MarkerOptions()
                                        .position(latLng)
                                        .title(title)
                                        .snippet(content));
                mMarkerToPostId.put(marker.getId(), post.getInt("id"));
            }
        }
        catch (JSONException e)
        {
            Log.d(TAG, "JSON Exception: " + e);
        }
    }

    @Override
    protected void onStop()
    {
        super.onStop();
        mLocManage.removeUpdates(mLocListen);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.activity_maps, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        switch (item.getItemId())
        {
            case R.id.action_get_spotposts:
                getSpotPosts();
                return true;
            case R.id.action_post_spotpost:
                Intent intent = new Intent(this, PostActivity.class);
                intent.putExtra(EXTRA_LATITUDE, mLat);
                intent.putExtra(EXTRA_LONGITUDE, mLng);
                startActivity(intent);
                return true;
            case R.id.action_logout:
                SpotpostClient.logout(new AsyncHttpResponseHandler()
                {
                    @Override
                    public void onSuccess(int i, Header[] headers, byte[] bytes)
                    {
                        Log.d(TAG, "Logout was successful");
                        Intent intent = new Intent(MapsActivity.this, LoginActivity.class);
                        MapsActivity.this.startActivity(intent);
                    }

                    @Override
                    public void onFailure(int i, Header[] headers, byte[] bytes, Throwable throwable)
                    {
                        Log.d(TAG, "Logout failed. Oh well.");
                        Intent intent = new Intent(MapsActivity.this, LoginActivity.class);
                        MapsActivity.this.startActivity(intent);
                    }
                });
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }
}
