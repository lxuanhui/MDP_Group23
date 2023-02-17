package com.example.mdp.chat;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.text.method.ScrollingMovementMethod;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.TextView;

import com.example.mdp.MainActivity;
import com.example.mdp.R;
import com.example.mdp.bluetooth.OnBluetoothReadReceivedListener;
import com.example.mdp.databinding.FragmentChatBinding;
import com.example.mdp.databinding.FragmentMainBinding;

import java.util.LinkedHashMap;

public class ChatFragment extends Fragment {
    private FragmentChatBinding binding;
    private TextView tvChat;
    private EditText etMessage;
    private ImageButton btnSend;

    public ChatFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        binding = FragmentChatBinding.inflate(inflater, container, false);
        return binding.getRoot();
    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        tvChat = binding.messageReceivedTitleTextView;
        etMessage = binding.typeBoxEditText;
        btnSend = binding.messageButton;

        tvChat.setMovementMethod(new ScrollingMovementMethod());

        btnSend.setOnClickListener(v -> {
            String message = etMessage.getText().toString();
            etMessage.setText("");
            if (!message.equals("")) {
                updateChatBox("APP", message);
                ((MainActivity) requireActivity()).getBluetoothService().write(message);
            }
        });

        ((MainActivity) requireActivity()).setChatReadListener(message -> updateChatBox("ROBOT", message));
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

    private void updateChatBox(String owner, String text) {
        String chat = "[" + owner + "]" + " " + text + "\n";
        tvChat.append(chat);
    }
}
