package com.example.mdp.arena;

import android.content.Context;
import android.widget.GridView;

import java.util.ArrayList;
import java.util.List;

public class GridArena {


    private final int numCol;
    private final int numRow;
    private List<Cell> grid;

    public GridArena(int numCol, int numRow) {
        this.numCol = numCol;
        this.numRow = numRow;

        // Make a list of cells in the grid with additional cells for displaying coordinates
        grid = new ArrayList<>();
        for (int i = 0; i < (numCol+1) * (numRow+1); i++) {
            grid.add(new Cell());
        }

    }

    public int toIndex(int xPos, int yPos){
        return xPos + (yPos *  (numCol+1));
    }

    public int[] toCoord(int index){
        int y = index / (numCol+1);
        int x = index % (numCol+1);
        return new int[]{x,y};
    }

    public int[] getNextDirCoord(int direction, int xPos, int yPos){
        return null; //TODO
    }

    public Cell cellAt(int x, int y) {
        if (x < 1 || x >= (numCol+1) || y < 1 || y >= (numRow+1)){
            return null;
        }
        return grid.get(toIndex(x,y));
    }

    public int getNumCol() {
        return numCol;
    }

    public int getNumRow() {
        return numRow;
    }

    public List<Cell> getGrid() {
        return grid;
    }
}
