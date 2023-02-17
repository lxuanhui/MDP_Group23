package com.example.mdp.arena;

public interface DragListener {
    public void onDragMove(int obsId, int[] oldPos, int[] newPos);
    public void onDragRemove(int obsId, int[] oldPos);
}
