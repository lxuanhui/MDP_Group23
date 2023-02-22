package com.example.mdp.arena;

import android.widget.ImageView;

public class Player {
    private final float startX;
    private final float startY;
    ImageView car;
    int[] carCoord = new int[2];
    Directions carDir;

    public Player(ImageView car, float startX, float startY){
        this.car = car;
        this.carCoord[0] = 1;
        this.carCoord[1] = 0;
        this.carDir = Directions.NORTH;

        this.startX = startX;
        this.startY = startY;
    }

    public int getAdapterPos(){
        return (19 - carCoord[1]) * 21 + (carCoord[0] + 1);

    }

    public int[] getAllAdapterPos(){
        int adapterpos = getAdapterPos();
        System.out.println(adapterpos);
        return new int[]{adapterpos - 22, adapterpos -21, adapterpos - 1, adapterpos};
    }

    public float getStartX() {
        return startX;
    }

    public float getStartY() {
        return startY;
    }

    public ImageView getCar() {
        return car;
    }

    public int[] getCarCoord() {
        return carCoord;
    }

    public Directions getCarDir() {
        return carDir;
    }

    public void setCarCoord(int[] carCoord) {
        this.carCoord = carCoord;
    }

    public void setCarDir(Directions carDir) {
        this.carDir = carDir;
    }
}
