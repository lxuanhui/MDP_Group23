package com.example.mdp.bluetooth;

import android.bluetooth.BluetoothDevice;

public interface OnBluetoothStateChangedListener {
    void onDisconnect();
    void onConnect(BluetoothDevice bluetoothDevice);
}
