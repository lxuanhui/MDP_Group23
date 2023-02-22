package com.example.mdp.bluetooth.receivers;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public class BluetoothScanBroadcastReceiver extends BroadcastReceiver {
    private static final String TAG = "MDP-BluetoothScanBroadcastReceiver";

    public interface BluetoothScanBroadcastReceiverCallback {
        void onConnected();
    }

    private BluetoothScanBroadcastReceiver.BluetoothScanBroadcastReceiverCallback callback;

    public BluetoothScanBroadcastReceiver(BluetoothScanBroadcastReceiver.BluetoothScanBroadcastReceiverCallback callback) {
        this.callback = callback;
    }

    public BluetoothScanBroadcastReceiver() {
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        final String action = intent.getAction();
        if (action.equals(BluetoothAdapter.ACTION_SCAN_MODE_CHANGED)) {
            final int mode = intent.getIntExtra(BluetoothAdapter.EXTRA_SCAN_MODE, BluetoothAdapter.ERROR);
            final int prev_mode = intent.getIntExtra(BluetoothAdapter.EXTRA_PREVIOUS_SCAN_MODE, BluetoothAdapter.ERROR);
            switch (mode) {
                // The device is in discoverable mode.
                case BluetoothAdapter.SCAN_MODE_CONNECTABLE_DISCOVERABLE:
                    Log.d(TAG, "SCAN_MODE_CONNECTABLE_DISCOVERABLE");
                    break;
                // The device isn't in discoverable mode but can still receive connections.
                case BluetoothAdapter.SCAN_MODE_CONNECTABLE:
                    Log.d(TAG, "SCAN_MODE_CONNECTABLE");
                    break;
                // The device isn't in discoverable mode and cannot receive connections.
                case BluetoothAdapter.SCAN_MODE_NONE:
                    Log.d(TAG, "SCAN_MODE_NONE");
                    break;
                default:
                    Log.d(TAG, "ERROR");
                    break;
            }
        }
    }
}
