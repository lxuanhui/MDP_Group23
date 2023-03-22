package com.example.mdp.arena;

public class Cell {
//    public static final int NORTH = 0;
//    public static final int EAST = 1;
//    public static final int SOUTH = 2;
//    public static final int WEST = 3;
    private int obstacleID;
    private int imgID;
    private Directions imgDir;
//    private boolean carFront;
//    private boolean carBack;
    private int adapterPos;

    //non-obstacle cell img id & obstacleId = -1
    //
    public Cell(){
        this.obstacleID = -1;
        this.imgID = -1;
//        this.carFront = false;
//        this.carBack = false;
        this.adapterPos = -1;
        this.imgDir = Directions.EAST;
    }

    public int getImgID() {
        return imgID;
    }

    public int getObstacleID() {
        return obstacleID;
    }

//    public boolean isCarBack() {
//        return carBack;
//    }
//
//    public boolean isCarFront() {
//        return carFront;
//    }


    public int getAdapterPos() {
        return adapterPos;
    }

    public Directions getImgDir() {
        return imgDir;
    }

    public void setImgID(int imgID) {this.imgID = imgID;}

    public void setObstacleID(int obstacleID) {
        this.obstacleID = obstacleID;
    }

//    public void setCarBack(boolean carBack) {
//        this.carBack = carBack;
//    }
//
//    public void setCarFront(boolean carFront) {
//        this.carFront = carFront;
//    }


    public void setAdapterPos(int adapterPos) {
        this.adapterPos = adapterPos;
    }

    public void setImgDir(Directions imgDir) {
        this.imgDir = imgDir;
    }
}
