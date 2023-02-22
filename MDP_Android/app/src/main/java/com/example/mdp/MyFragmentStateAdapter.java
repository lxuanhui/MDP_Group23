package com.example.mdp;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.recyclerview.widget.RecyclerView;
import androidx.viewpager2.adapter.FragmentStateAdapter;

import com.example.mdp.arena.Cell;
import com.example.mdp.arena.OnCellClickListener;
import com.example.mdp.arena.Player;
import com.example.mdp.arena.RecyclerAdapter;
import com.example.mdp.chat.ChatFragment;
import com.example.mdp.timer.TimerFragment;

import java.util.List;

public class MyFragmentStateAdapter extends FragmentStateAdapter {


    private Player carPlayer;
    //    public MyFragmentStateAdapter(MainActivity mainActivity) {
//    }
    RecyclerView gridRecyclerView;
    RecyclerAdapter gridRecyclerAdapter;
    private List<Cell> grid;
    public MyFragmentStateAdapter(@NonNull FragmentActivity fragmentActivity, RecyclerView gridRecyclerView,RecyclerAdapter recycleradapter, List<Cell> grid, Player carPlayer) {
        super(fragmentActivity);
        this.gridRecyclerView = gridRecyclerView;
        this.gridRecyclerAdapter = recycleradapter;
        this.grid = grid;
        this.carPlayer = carPlayer;
    }

    @NonNull
    @Override
    public Fragment createFragment(int position) {
        switch (position) {
                case 0:
                    return new MapTabFragment(gridRecyclerView, carPlayer);
                case 1:
                    return new ChatFragment();
                case 2:
                   return new TimerFragment();
                default:
                   return new MainFragment();
            }
    }

    @Override
    public int getItemCount() {
        return 3;
    }
}
