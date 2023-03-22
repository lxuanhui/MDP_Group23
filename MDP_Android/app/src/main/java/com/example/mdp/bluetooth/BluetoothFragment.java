package com.example.mdp.bluetooth;

import android.Manifest.permission;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.DialogFragment;
import androidx.navigation.fragment.NavHostFragment;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.mdp.MainActivity;
import com.example.mdp.R;
import com.example.mdp.bluetooth.receivers.BluetoothDiscoveryBroadcastReceiver;
import com.example.mdp.bluetooth.service.BluetoothService;
import com.example.mdp.databinding.FragmentBluetoothBinding;

import java.util.ArrayList;
import java.util.Optional;
import java.util.Set;

public class BluetoothFragment extends DialogFragment {
    private static final String TAG = "MDP-BluetoothFragment";

    private final String[] permissions1 = { permission.BLUETOOTH_SCAN, permission.BLUETOOTH_CONNECT, permission.ACCESS_FINE_LOCATION, permission.ACCESS_COARSE_LOCATION, };
    private final String[] permissions2 = { permission.BLUETOOTH, permission.BLUETOOTH_ADMIN, permission.ACCESS_FINE_LOCATION, permission.ACCESS_COARSE_LOCATION, };
    private final String[] permissions = (android.os.Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) ? permissions1 : permissions2;

    private FragmentBluetoothBinding binding;

    private BluetoothAdapter bluetoothAdapter;
    private BluetoothRecyclerViewAdapter adapter;
    private ArrayList<BluetoothDevice> devices;
    private BluetoothDiscoveryBroadcastReceiver discoveryReceiver;
    private BluetoothService bluetoothService;

    public BluetoothFragment(BluetoothService bluetoothService) {
        this.bluetoothService = bluetoothService;
    }

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        Log.d(TAG, "onCreateView()");
        binding = FragmentBluetoothBinding.inflate(inflater, container, false);
        return binding.getRoot();
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        Log.d(TAG, "onViewCreated()");
        super.onViewCreated(view, savedInstanceState);

        if (hasPermissions()) {
            init();
        } else {
            requestPermissions();
        }
    }


    @Override
    public void onStart() {
        Log.d(TAG, "onStart()");
        super.onStart();
        if (getDialog() != null) {
            getDialog().getWindow().setLayout(600, 1000);
        }
    }

    @Override
    public void onDestroyView() {
        Log.d(TAG, "onDestroyView()");
        super.onDestroyView();
        binding = null;
        if (ActivityCompat.checkSelfPermission(requireActivity(), permission.BLUETOOTH_SCAN) == PackageManager.PERMISSION_GRANTED) {
            if (bluetoothAdapter != null) {
                bluetoothAdapter.cancelDiscovery();
            }
        }
        if (discoveryReceiver != null) {
            requireActivity().unregisterReceiver(discoveryReceiver);
        }
    }

    private boolean hasPermissions() {
        for (String permission : permissions) {
            if (ActivityCompat.checkSelfPermission(requireActivity(), permission) != PackageManager.PERMISSION_GRANTED) {
                Log.d(TAG, permission);
                return false;
            }
        }
        return true;
    }

    private void requestPermissions() {
        registerForActivityResult(new ActivityResultContracts.RequestMultiplePermissions(), isGranted -> {
            if (isGranted.containsValue(false)) {
                showPermissionsDialog();
            } else {
                init();
            }
        }).launch(permissions);
    }

    private void showPermissionsDialog() {
        AlertDialog alertDialog = new AlertDialog.Builder(requireActivity()).create();
        alertDialog.setTitle("No required permissions");
        alertDialog.setMessage("Application does not work without the required permissions.");
        alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK", (dialog, which) -> dialog.dismiss());
        alertDialog.show();
    }

    private void initBluetoothAdapter() {
        // Retrieve BluetoothAdapter
        BluetoothManager bluetoothManager = requireActivity().getSystemService(BluetoothManager.class);
        bluetoothAdapter = bluetoothManager.getAdapter();

        // Enable Bluetooth
        if (!bluetoothAdapter.isEnabled()) {
            Intent intent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == Activity.RESULT_OK) {
                    init();
                } else {
                    showPermissionsDialog();
                }
            }).launch(intent);
        }
    }

    private void initRecyclerView() {
        RecyclerView recyclerView = binding.listDevices;
        LinearLayoutManager layoutManager =  (LinearLayoutManager) Optional.ofNullable(recyclerView.getLayoutManager()).orElse(new LinearLayoutManager(requireActivity()));
        int scrollPosition = layoutManager.findFirstCompletelyVisibleItemPosition();
        recyclerView.setLayoutManager(layoutManager);
        recyclerView.scrollToPosition(scrollPosition);

        @SuppressLint("MissingPermission") View.OnClickListener listener = v -> {
            int position = recyclerView.getChildLayoutPosition(v);
            BluetoothDevice device = devices.get(position);
            BluetoothService service = ((MainActivity) requireActivity()).getBluetoothService();
            service.connect(device);
            Toast.makeText(getContext(), "Connecting to " + device.getName(), Toast.LENGTH_SHORT).show();
            dismiss();
            // NavHostFragment.findNavController(BluetoothFragment.this).navigate(R.id.action_BluetoothFragment_to_MainFragment);
        };
        adapter = new BluetoothRecyclerViewAdapter(devices, listener);
        recyclerView.setAdapter(adapter);
        DividerItemDecoration dividerItemDecoration = new DividerItemDecoration(recyclerView.getContext(), layoutManager.getOrientation());
        recyclerView.addItemDecoration(dividerItemDecoration);
    }

    @SuppressLint("MissingPermission")
    private void initDevices() {
        Set<BluetoothDevice> bondedDevices = bluetoothAdapter.getBondedDevices();
        devices.addAll(bondedDevices);
        adapter.notifyItemInserted(devices.size() - 1);
    }

    @SuppressLint("MissingPermission")
    private void discoverDevices() {
        discoveryReceiver = new BluetoothDiscoveryBroadcastReceiver(device -> {
            devices.add(device);
            adapter.notifyItemInserted(devices.size() - 1);
        });
        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        requireActivity().registerReceiver(discoveryReceiver, filter);
        bluetoothAdapter.startDiscovery();
    }

    private void makeDiscoverable() {
        Intent intent = new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE);
        registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
            if (result.getResultCode() == Activity.RESULT_CANCELED) {
                Log.d(TAG, "ACTION_REQUEST_DISCOVERABLE - RESULT_CANCELED");
            } else {
                Log.d(TAG, "ACTION_REQUEST_DISCOVERABLE - SUCCESS");
                bluetoothService.accept();
            }
        }).launch(intent);
    }

    private void init() {
        devices = new ArrayList<>();
        initRecyclerView();
        initBluetoothAdapter();
        makeDiscoverable();
        initDevices();
        discoverDevices();
    }
}
