package com.example.mdp.bluetooth.service;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.util.Log;

import com.example.mdp.bluetooth.Constants;
import com.example.mdp.bluetooth.OnBluetoothReadReceivedListener;
import com.example.mdp.bluetooth.OnBluetoothStateChangedListener;

import java.io.IOException;

public class BluetoothAcceptThread extends BluetoothSocketThread {
    private static final String TAG = "MDP-BluetoothAcceptThread";

    private final BluetoothServerSocket serverSocket;

    @SuppressLint("MissingPermission")
    private BluetoothAcceptThread(BluetoothAdapter adapter) {
        BluetoothServerSocket serverSocket = null;
        try {
            serverSocket = adapter.listenUsingRfcommWithServiceRecord(Constants.name, Constants.uuid);
            Log.d(TAG, "listenUsingRfcommWithServiceRecord() success");
        } catch (IOException e) {
            Log.d(TAG, "listenUsingRfcommWithServiceRecord() exception");
        }
        this.serverSocket = serverSocket;
    }

    private OnBluetoothReadReceivedListener readListener;
    public BluetoothAcceptThread(BluetoothAdapter adapter, OnBluetoothReadReceivedListener readListener, OnBluetoothStateChangedListener stateListener) {
        this(adapter);
        this.readListener = readListener;
        this.stateListener = stateListener;
    }

    public void run() {
        while (true) {
            try {
                socket = serverSocket.accept();
                new BluetoothConnectedThread(socket, readListener, stateListener).start();
                stateListener.onConnect(socket.getRemoteDevice());
                Log.d(TAG, "accept() success");
            } catch (IOException e) {
                Log.d(TAG, "accept() exception");
                break;
            }
        }
    }

    @Override
    public void cancel() {
        try {
            if (serverSocket != null) {
                serverSocket.close();
                Log.d(TAG, "serverSocket close() success");
            }
        } catch (IOException e) {
            Log.d(TAG, "serverSocket close() exception");
        }
        super.cancel();
    }

    @Override
    public String getType() {
        return "Accept";
    }
}
