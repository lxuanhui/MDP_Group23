package com.example.mdp.bluetooth.receivers;

import android.bluetooth.BluetoothAdapter;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public class BluetoothConnectionStateBroadcastReceiver extends BroadcastReceiver {
    private static final String TAG = "MDP-BluetoothConnectionStateBroadcastReceiver";

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.d(TAG, "onReceive()");
        final String action = intent.getAction();
        if (action.equals(BluetoothAdapter.ACTION_CONNECTION_STATE_CHANGED)) {
            final int state = intent.getIntExtra(BluetoothAdapter.EXTRA_CONNECTION_STATE, BluetoothAdapter.ERROR);
            final int prev_state = intent.getIntExtra(BluetoothAdapter.EXTRA_PREVIOUS_CONNECTION_STATE, BluetoothAdapter.ERROR);
            switch (state) {
                case BluetoothAdapter.STATE_DISCONNECTED:
                    Log.d(TAG, "STATE_DISCONNECTED");
                    break;
                case BluetoothAdapter.STATE_DISCONNECTING:
                    Log.d(TAG, "STATE_DISCONNECTING");
                    break;
                case BluetoothAdapter.STATE_CONNECTED:
                    Log.d(TAG, "STATE_CONNECTED");
                    break;
                case BluetoothAdapter.STATE_CONNECTING:
                    Log.d(TAG, "STATE_CONNECTING");
                    break;
                default:
                    Log.d(TAG, "ERROR");
                    break;
            }
        }
    }
}
