package com.example.mdp;

import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModel;
import androidx.recyclerview.widget.RecyclerView;

import com.example.mdp.arena.RecyclerAdapter;

public class SharedViewModel extends ViewModel {
    private OnDataPass callback;
    private RecyclerAdapter gridRecyclerAdapter;
//    private RecyclerView gridRecyclerView;
    private Fragment mapFragment;

    private int[][] obstacles;
    // other data

    public void setCallback(OnDataPass callback) {
        this.callback = callback;
    }

    public OnDataPass getCallback() {
        return callback;
    }
    //getter and setter for other data


    public RecyclerAdapter getGridRecyclerAdapter() {
        return gridRecyclerAdapter;
    }

    public void setGridRecyclerAdapter(RecyclerAdapter gridRecyclerAdapter) {
        this.gridRecyclerAdapter = gridRecyclerAdapter;
    }
//
//    public RecyclerView getGridRecyclerView() {
//        return gridRecyclerView;
//    }
//
//    public void setGridRecyclerView(RecyclerView gridRecyclerView) {
//        this.gridRecyclerView = gridRecyclerView;
//    }

    public Fragment getMapFragment() {
        return mapFragment;
    }

    public void setMapFragment(Fragment mapFragment) {
        this.mapFragment = mapFragment;
    }

    public int[][] getObstacles() {
        return obstacles;
    }

    public void setObstacles(int[][] obstacles) {
        this.obstacles = obstacles;
    }
}

