package com.example.mdp.bluetooth.service;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.util.Log;

import com.example.mdp.bluetooth.OnBluetoothReadReceivedListener;
import com.example.mdp.bluetooth.OnBluetoothStateChangedListener;

import java.util.Objects;

public class BluetoothService {
    private static final String TAG = "MDP-BluetoothService";

    public static final int STATE_IDLE = 0;
    public static final int STATE_CONNECTED = 1;

    private final BluetoothAdapter adapter;
    private BluetoothSocketThread socketThread;
    private BluetoothConnectedThread readThread;
    private BluetoothConnectedThread writeThread;
    private final OnBluetoothReadReceivedListener readListener;
    private final OnBluetoothStateChangedListener stateListener;
    private int state;
    private BluetoothDevice device;

    public BluetoothService(OnBluetoothReadReceivedListener readListener, OnBluetoothStateChangedListener stateListener) {
        this.adapter = BluetoothAdapter.getDefaultAdapter();
        this.socketThread = null;
        this.readThread = null;
        this.writeThread = null;
        this.readListener = readListener;
        this.stateListener = new OnBluetoothStateChangedListener() {
            @Override
            public void onDisconnect() {
                stateListener.onDisconnect();
                state = STATE_IDLE;
            }

            @Override
            public void onConnect(BluetoothDevice bluetoothDevice) {
                stateListener.onConnect(bluetoothDevice);
                state = STATE_CONNECTED;
                device = bluetoothDevice;
            }
        };
        this.state = STATE_IDLE;
        this.device = null;
    }

    // As server
    public synchronized void accept() {
        Log.d(TAG, "accept()");

        if (socketThread != null) {
            socketThread.cancel();
        }
        socketThread = new BluetoothAcceptThread(adapter, readListener, stateListener);
        socketThread.start();
    }

    // As client
    public synchronized void connect(BluetoothDevice device) {
        Log.d(TAG, "connect()");

        if (socketThread != null) {
            socketThread.cancel();
        }
        socketThread = new BluetoothConnectThread(adapter, device, readListener, stateListener);
        socketThread.start();
    }

    public synchronized void reconnect() {
        if (canReconnect()) {
            Log.d(TAG, "reconnect()");
            socketThread = new BluetoothConnectThread(adapter, device, readListener, stateListener);
            socketThread.start();
        }
    }

    public synchronized void write(String message) {
        Log.d(TAG, "write!()");

        if (state == STATE_CONNECTED && socketThread != null) {
            message += "#";
            //HI
            writeThread = new BluetoothConnectedThread(socketThread.getSocket(), message);
            writeThread.start();
        }
    }

    public synchronized void read() {
        Log.d(TAG, "read()");

        if (state == STATE_CONNECTED && socketThread != null) {
            readThread = new BluetoothConnectedThread(socketThread.getSocket(), readListener, stateListener);
            readThread.start();
        }
    }
    public synchronized void stop() {
        Log.d(TAG, "stop()");

        if (socketThread != null) {
            socketThread.cancel();
        }

        socketThread = null;
        writeThread = null;
        readThread = null;
        state = STATE_IDLE;
        device = null;
    }

    public int getState() {
        return state;
    }

    public BluetoothDevice getDevice() {
        return device;
    }

    public boolean canReconnect() {
        return device != null && socketThread != null && Objects.equals(socketThread.getType(), "Connect");
    }
}
