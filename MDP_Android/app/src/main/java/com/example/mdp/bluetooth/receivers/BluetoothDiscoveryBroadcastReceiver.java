package com.example.mdp.bluetooth.receivers;

import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public class BluetoothDiscoveryBroadcastReceiver extends BroadcastReceiver {
    private static final String TAG = "MDP-BluetoothDiscoveryBroadcastReceiver";

    public interface BluetoothDiscoveryBroadcastReceiverCallback {
        void onDiscovered(BluetoothDevice device);
    }

    private BluetoothDiscoveryBroadcastReceiverCallback callback;

    public BluetoothDiscoveryBroadcastReceiver(BluetoothDiscoveryBroadcastReceiverCallback callback) {
        this.callback = callback;
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        final String action = intent.getAction();
        if (action.equals(BluetoothDevice.ACTION_FOUND)) {
            Log.d(TAG, "ACTION_FOUND");
            BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
            callback.onDiscovered(device);
        }
    }
}
