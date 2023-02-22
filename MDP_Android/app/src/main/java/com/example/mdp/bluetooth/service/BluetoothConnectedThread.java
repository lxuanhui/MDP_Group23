package com.example.mdp.bluetooth.service;

import android.bluetooth.BluetoothSocket;
import android.util.Log;

import com.example.mdp.bluetooth.OnBluetoothReadReceivedListener;
import com.example.mdp.bluetooth.OnBluetoothStateChangedListener;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class BluetoothConnectedThread extends Thread {
    private static final String TAG = "MDP-BluetoothConnectedThread";

    private final BluetoothSocket socket;
    private final InputStream in;
    private final OutputStream out;

    private String message = null;
    private OnBluetoothReadReceivedListener readListener = null;
    private OnBluetoothStateChangedListener stateListener = null;


    private BluetoothConnectedThread(BluetoothSocket socket) {
        InputStream in = null;
        OutputStream out = null;

        try {
            in = socket.getInputStream();
            Log.d(TAG, "getInputStream() success");
        } catch (IOException e) {
            Log.d(TAG, "getInputStream() exception");
        }
        try {
            out = socket.getOutputStream();
            Log.d(TAG, "getOutputStream() success");
        } catch (IOException e) {
            Log.d(TAG, "getOutputStream() exception");
        }

        this.socket = socket;
        this.in = in;
        this.out = out;
    }

    public BluetoothConnectedThread(BluetoothSocket socket,
                                    OnBluetoothReadReceivedListener readListener,
                                    OnBluetoothStateChangedListener stateListener) {
        this(socket);
        this.readListener = readListener;
        this.stateListener = stateListener;
    }

    public BluetoothConnectedThread(BluetoothSocket socket, String message) {
        this(socket);
        this.message = message;
    }

    public void run() {
        if (message != null) {
            write(message.getBytes());
        } else {
            read();
        }
    }

    public void read() {
        while (true) {
            try {
                byte[] buffer = new byte[1024];
                in.read(buffer);
                readListener.onBluetoothReadReceived(new String(buffer));
                Log.d(TAG, "read() success");
            } catch (IOException e) {
                Log.d(TAG, "read() exception");
                stateListener.onDisconnect();
                break;
            }
        }
    }

    public void write(byte[] bytes) {
        try {
            out.write(bytes);
            Log.d(TAG, "write() success");
        } catch (IOException e) {
            Log.d(TAG, e.toString());
        }
    }
}


