package com.example.mdp.bluetooth;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothDevice;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.mdp.R;

import java.util.ArrayList;

public class BluetoothRecyclerViewAdapter extends RecyclerView.Adapter<BluetoothRecyclerViewAdapter.ViewHolder> {
    private final ArrayList<BluetoothDevice> data;
    private final View.OnClickListener listener;

    public BluetoothRecyclerViewAdapter(ArrayList<BluetoothDevice> data, View.OnClickListener listener) {
        this.data = data;
        this.listener = listener;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(ViewGroup viewGroup, int viewType) {
        // Create a new view, which defines the UI of the list item
        View view = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.content_bluetooth, viewGroup, false);
        return new ViewHolder(view);
    }

    @SuppressLint("MissingPermission")
    @Override
    public void onBindViewHolder(ViewHolder viewHolder, final int position) {
        BluetoothDevice device = data.get(position);
        viewHolder.getTvName().setText(device.getName());
        viewHolder.getTvAddress().setText(device.getAddress());
        String state = device.getBondState() == BluetoothDevice.BOND_NONE ? "UNPAIRED" : "PAIRED";
        viewHolder.getTvState().setText(state);
        viewHolder.itemView.setOnClickListener(listener);
    }

    @Override
    public int getItemCount() {
        return data.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        private final TextView tvName;
        private final TextView tvAddress;
        private final TextView tvState;

        public ViewHolder(View view) {
            super(view);
            // Define click listener for the ViewHolder's View
            tvName = (TextView) view.findViewById(R.id.tvName);
            tvAddress = (TextView) view.findViewById(R.id.tvAddress);
            tvState = (TextView) view.findViewById(R.id.tvState);
        }

        public TextView getTvName() {
            return tvName;
        }

        public TextView getTvAddress() {
            return tvAddress;
        }

        public TextView getTvState() {
            return tvState;
        }
    }
}
