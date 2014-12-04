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
import android.view.View;
import android.view.ViewTreeObserver;
import android.widget.FrameLayout;
import android.widget.ProgressBar;

import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.loopj.android.http.JsonHttpResponseHandler;

import org.apache.http.Header;
import org.json.JSONException;
import org.json.JSONObject;

public class MapsActivity extends FragmentActivity
{
    private static final String TAG = "MapsActivity";

    private GoogleMap mMap; // Might be null if Google Play services APK is not available.
    private View mProgressView;
    private LocationManager mLocManage;
    private LocationListener mLocListen;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);

        setUpMapIfNeeded();
        mProgressView = setupProgressBar();
        mLocManage = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        setupMapLoc();
        mLocListen = setupLocListen();
        SpotpostClient.setup(this);
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
        LatLng latLng = new LatLng(loc.getLatitude(), loc.getLongitude());
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
                LatLng latLng = new LatLng(location.getLatitude(), location.getLongitude());
                CameraUpdate camUpdate = CameraUpdateFactory.newLatLng(latLng);
                mMap.animateCamera(camUpdate);
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
            public void onProviderEnabled(String provider) {}

            @Override
            public void onProviderDisabled(String provider) {}
        };
    }

    @Override
    protected void onResume()
    {
        super.onResume();
        setUpMapIfNeeded();
        mLocManage.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000, 0, mLocListen);
        SpotpostClient.isLoggedIn(new JsonHttpResponseHandler()
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
                    Log.d(TAG, "JSON Response: " + response.toString(2));

                    if (response.getJSONObject("error").getInt("code") != 1000)
                    {
                        Intent intent = new Intent(MapsActivity.this, LoginActivity.class);
                        MapsActivity.this.startActivity(intent);
                    }
                    else
                    {
                        Log.d(TAG, "User is already logged in");
                    }
                }
                catch (JSONException e)
                {
                    Log.d(TAG, "JSON Exception: " + e);
                    Log.d(TAG, "Couldn't determine login state");
                    return;
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, String responseString, Throwable error)
            {
                Log.d(TAG, "Login Check HTTP Failure: " + responseString, error);
                Log.d(TAG, "Couldn't determine login state");
            }

            @Override
            public void onFinish ()
            {
                mProgressView.setVisibility(View.INVISIBLE);
            }
        });
    }

    @Override
    protected void onPause()
    {
        super.onPause();
        mLocManage.removeUpdates(mLocListen);
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
    }
}
