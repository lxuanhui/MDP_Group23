package com.example.mdp.bluetooth.service;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.util.Log;

import com.example.mdp.bluetooth.Constants;
import com.example.mdp.bluetooth.OnBluetoothReadReceivedListener;
import com.example.mdp.bluetooth.OnBluetoothStateChangedListener;

import java.io.IOException;

public class BluetoothConnectThread extends BluetoothSocketThread {
    private static final String TAG = "MDP-BluetoothConnectThread";

    private final BluetoothAdapter adapter;

    @SuppressLint("MissingPermission")
    private BluetoothConnectThread(BluetoothAdapter adapter, BluetoothDevice device) {
        BluetoothSocket socket = null;
        try {
            socket = device.createRfcommSocketToServiceRecord(Constants.uuid);
            Log.d(TAG, "createRfcommSocketToServiceRecord() success");
        } catch (IOException e) {
            Log.d(TAG, "createRfcommSocketToServiceRecord() exception");
        }
        this.socket = socket;
        this.adapter = adapter;
    }

    private OnBluetoothReadReceivedListener readListener;
    public BluetoothConnectThread(BluetoothAdapter adapter,
                                  BluetoothDevice device,
                                  OnBluetoothReadReceivedListener readListener,
                                  OnBluetoothStateChangedListener stateListener) {
        this(adapter, device);
        this.readListener = readListener;
        this.stateListener = stateListener;
    }

    @SuppressLint("MissingPermission")
    public void run() {
        adapter.cancelDiscovery();

        try {
            socket.connect();
            new BluetoothConnectedThread(socket, readListener, stateListener).start();
            stateListener.onConnect(socket.getRemoteDevice());
            Log.d(TAG, "connect() success");
        } catch (IOException connectException) {
            try {
                Log.d(TAG, "connect() exception");
                socket.close();
            } catch (IOException closeException) {
                Log.d(TAG, "close() exception");
            }
            stateListener.onDisconnect();
        }
    }

    public String getType() {
        return "Connect";
    }
}
