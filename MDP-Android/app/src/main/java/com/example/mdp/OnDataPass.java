package com.example.mdp;

import androidx.recyclerview.widget.RecyclerView;

import com.example.mdp.arena.Directions;
import com.example.mdp.arena.RecyclerAdapter;

public interface OnDataPass {
    public void OnObsPass(int obsId, int[] oldPos, int[] newPos);
    public void OnAddObs(int obsId, int[] pos);
    public void OnSetCar();
    public void OnSetCarDir();
    public void OnResetMap();
    public void changeImgDir(int obsId, Directions newImgDir, int newImgId);
    public void OnSendMap();
}
