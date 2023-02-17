package com.example.mdp.bluetooth.receivers;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public class BluetoothBondStateBroadcastReceiver extends BroadcastReceiver {
    private static final String TAG = "MDP-BluetoothBondStateBroadcastReceiver";

    @SuppressLint("MissingPermission")
    @Override
    public void onReceive(Context context, Intent intent) {
        final String action = intent.getAction();
        if (action.equals(BluetoothDevice.ACTION_BOND_STATE_CHANGED)) {
            BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
            final int state = device.getBondState();
            switch (state) {
                case BluetoothDevice.BOND_NONE:
                    Log.d(TAG, "BOND_NONE");
                    break;
                case BluetoothDevice.BOND_BONDING:
                    Log.d(TAG, "BOND_BONDING");
                    break;
                case BluetoothDevice.BOND_BONDED:
                    Log.d(TAG, "BOND_BONDED");
                    break;
            }
        }
    }
}
