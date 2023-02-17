package com.example.mdp.arena;

import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.mdp.R;

import java.util.Collections;
import java.util.List;

public class RecyclerAdapter extends RecyclerView.Adapter<RecyclerAdapter.MineTileViewHolder> {
    private List<Cell> grid;
    private OnCellClickListener listener;
    private boolean setLongClick;

    public RecyclerAdapter(List<Cell> grid, OnCellClickListener listener){
        this.grid = grid;
        this.listener = listener;
        this.setLongClick = true;
    }
    @NonNull
    @Override
    public RecyclerAdapter.MineTileViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_cell, parent, false);

        return new MineTileViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull RecyclerAdapter.MineTileViewHolder holder, int position) {
        holder.bind(grid.get(position));
        holder.setIsRecyclable(false);
    }

    @Override
    public int getItemCount() {
        return grid.size();
    }

    public void setGrid(List<Cell> grid) {
        this.grid = grid;
        notifyDataSetChanged();
    }

    public int getCellId(int position){
        Cell cell = grid.get(position);
        return cell.getObstacleID();

    }
    public boolean isObstacle(int xPos, int yPos){
        int layoutPos = (19 - yPos) * 21 + (xPos + 1);
        Cell cell = grid.get(layoutPos);
        return cell.getObstacleID() > 0;
    }

    public void swapItem(int oldPos, int newPos) {
        Cell temp = grid.get(oldPos);
        grid.set(oldPos, grid.get(newPos));
        grid.set(newPos, temp);
        notifyDataSetChanged();
//        Collections.swap(grid, oldPos, newPos);
//        notifyItemMoved(oldPos, newPos);
    }

    public void resetCell(int pos){
        Cell newCell = new Cell();
        grid.remove(pos);
        grid.add(pos, newCell);
        notifyItemChanged(pos);
//        notifyDataSetChanged();
    }

    public void setImgId(int imgId, int pos){
        Cell cell = grid.get(pos);
        cell.setImgID(imgId);
        notifyItemChanged(pos);
//        notifyDataSetChanged();

    }

    public void setLongClick(boolean setLongClick) {
        this.setLongClick = setLongClick;
    }

    // One Cell
    public class MineTileViewHolder extends RecyclerView.ViewHolder{
        TextView cellText;
        ImageView eastBar, westBar, northBar, southBar;

        int rowNo;
        int colNo;

        public MineTileViewHolder(@NonNull View itemView) {
            super(itemView);

            cellText = itemView.findViewById(R.id.cellText);
            eastBar = itemView.findViewById(R.id.eastBar);
            westBar = itemView.findViewById(R.id.westBar);
            northBar = itemView.findViewById(R.id.northBar);
            southBar = itemView.findViewById(R.id.southBar);

//            car = findViewById(R.id.Car);


        }

        public void bind(final Cell cell){
            rowNo = 19 - this.getLayoutPosition() / 21; //Y
            colNo = this.getLayoutPosition() % 21 - 1; //X
            // initial Empty Layout
            if(rowNo == -1 & colNo == -1) {
                itemView.setBackgroundColor(Color.TRANSPARENT);
            }
            else if (rowNo == -1) {
                itemView.setBackgroundColor(Color.TRANSPARENT);
                cellText.setText(Integer.toString(colNo));
                cellText.setTextColor(Color.BLACK);
            }
            else if (colNo == -1 ){
                itemView.setBackgroundColor(Color.TRANSPARENT);
                cellText.setText(Integer.toString(rowNo));
                cellText.setTextColor(Color.BLACK);
            }
            else {
                itemView.setBackgroundColor(Color.parseColor("#ffaaaaaa"));
                cellText.setText("");
            }
            northBar.setVisibility(View.INVISIBLE);
            eastBar.setVisibility(View.INVISIBLE);
            southBar.setVisibility(View.INVISIBLE);
            westBar.setVisibility(View.INVISIBLE);



            // If it is an obstacle
            if (cell.getObstacleID() > 0){

                //set the direction
                switch (cell.getImgDir()){
                    case NORTH:
                        northBar.setVisibility(View.VISIBLE);
                        break;
                    case EAST:
                        eastBar.setVisibility(View.VISIBLE);
                        break;
                    case SOUTH:
                        southBar.setVisibility(View.VISIBLE);
                        break;
                    case WEST:
                        westBar.setVisibility(View.VISIBLE);
                        break;
                    default:
                        throw new IllegalStateException("Unexpected value: " + cell.getImgDir());
                }
                //If image is recognised, show image id
                if (cell.getImgID() > 0) {
//                    itemView.setBackgroundColor(Color.YELLOW);
                    itemView.setBackgroundColor(Color.rgb(254,204,205));
                    cellText.setText(Integer.toString(cell.getImgID()));
                    cellText.setTextColor(Color.BLACK);
                    cellText.setTextSize(15);

                }
                //If image not recognised, show obstacle id
                else {
                    itemView.setBackgroundColor(Color.rgb(161,255,252));
                    cellText.setText(Integer.toString(cell.getObstacleID()));
                    cellText.setTextColor(Color.BLACK);
                    cellText.setTextSize(12);
                }
            }

            itemView.setOnClickListener((view) -> {
                listener.onCellClick(cell, this.getLayoutPosition());
//                car.animate().translationXBy(25);
            });
            itemView.setOnLongClickListener((view) -> {
                listener.onCellLongClick(cell, this.getLayoutPosition());
                return true;
            });
            itemView.setLongClickable(setLongClick);


        }

    }
}
