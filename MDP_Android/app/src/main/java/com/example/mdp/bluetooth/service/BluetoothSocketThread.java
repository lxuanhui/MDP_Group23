package com.example.mdp.bluetooth.service;

import android.bluetooth.BluetoothSocket;
import android.util.Log;

import com.example.mdp.bluetooth.OnBluetoothStateChangedListener;

import java.io.IOException;

public abstract class BluetoothSocketThread extends Thread {
    private static final String TAG = "MDP-BluetoothSocketThread";

    protected BluetoothSocket socket;
    protected OnBluetoothStateChangedListener stateListener;

    public BluetoothSocket getSocket() {
        return socket;
    }

    public void cancel() {
        try {
            if (socket != null) {
                socket.close();
                Log.d(TAG, "socket close() success");
            }
        } catch (IOException e) {
            Log.d(TAG, "socket close() exception");
        }
        stateListener.onDisconnect();
    }

    public abstract String getType();
}
