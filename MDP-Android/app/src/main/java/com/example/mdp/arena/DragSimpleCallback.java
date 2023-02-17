package com.example.mdp.arena;

import static java.lang.Math.max;

import android.content.Context;
import android.graphics.Canvas;
import android.util.TypedValue;
import android.view.View;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.ItemTouchHelper;
import androidx.recyclerview.widget.RecyclerView;

import com.example.mdp.MainActivity;

import java.util.Arrays;

// Source: https://stackoverflow.com/questions/58159346/how-to-create-recyclerview-drag-and-drop-swap-2-item-positions-version
public class DragSimpleCallback extends ItemTouchHelper.SimpleCallback {

    final int[] oldPos = new int[1];
    final int[] newPos = new int[1];
    private final RecyclerAdapter gridRecyclerAdapter;
    private boolean dragEnabled = false;
    private Context context;
    private DragListener listener;

    final int[] old = new int[2];
    final int[] newO = new int[2];
    boolean removed = false;
    boolean moved = false;
    int obsID;




    /**
     * Creates a Callback for the given drag and swipe allowance. These values serve as
     * defaults
     * and if you want to customize behavior per ViewHolder, you can override
     * {@link #getSwipeDirs(RecyclerView, ViewHolder)}
     * and / or {@link #getDragDirs(RecyclerView, ViewHolder)}.
     *
     * @param dragDirs  Binary OR of direction flags in which the Views can be dragged. Must be
     *                  composed of {@link #LEFT}, {@link #RIGHT}, {@link #START}, {@link
     *                  #END},
     *                  {@link #UP} and {@link #DOWN}.
     * @param swipeDirs Binary OR of direction flags in which the Views can be swiped. Must be
     *                  composed of {@link #LEFT}, {@link #RIGHT}, {@link #START}, {@link
     *                  #END},
     *                  {@link #UP} and {@link #DOWN}.
     */
    public DragSimpleCallback(RecyclerAdapter gridRecyclerAdapter, Context context, DragListener listener) {
        super(0,0);
        this.gridRecyclerAdapter = gridRecyclerAdapter;
        this.context = context;
        this.listener = listener;
        this.removed = false;
        this.moved = false;


    }

    public void setDragEnabled(boolean dragEnabled) {
        this.dragEnabled = dragEnabled;
    }

    @Override
    public int getMovementFlags(@NonNull RecyclerView recyclerView, @NonNull RecyclerView.ViewHolder viewHolder) {
        int oldA = viewHolder.getAdapterPosition();
        if (dragEnabled && gridRecyclerAdapter.getCellId(oldA) > 0) {
            int dragFlags = ItemTouchHelper.UP | ItemTouchHelper.DOWN | ItemTouchHelper.LEFT | ItemTouchHelper.RIGHT;
            return makeMovementFlags(dragFlags, 0);
        } else {
            return 0;
        }
    }

    @Override
    public boolean onMove(@NonNull RecyclerView recyclerView, @NonNull RecyclerView.ViewHolder viewHolder, @NonNull RecyclerView.ViewHolder target) {
        int newA = target.getAdapterPosition();
        int oldA = viewHolder.getAdapterPosition();
        obsID = gridRecyclerAdapter.getCellId(oldA);
        if (newA < 420 && newA %21 != 0  //target not in row or column -1
                && gridRecyclerAdapter.getCellId(oldA) > 0// only obstacles can be dragged
                && gridRecyclerAdapter.getCellId(newA) < 0) { // only drop to empty cells
            moved = true;

            oldPos[0] = oldA;
            newPos[0] = newA;

            old[0] = viewHolder.getLayoutPosition() % 21 - 1;
            old[1] = 19 - viewHolder.getLayoutPosition() / 21 ;

            newO[0] = target.getLayoutPosition() % 21 - 1;
            newO[1] = 19 - target.getLayoutPosition() / 21;

            return true;
        }
        return false;
    }

    @Override
    public void onSwiped(@NonNull RecyclerView.ViewHolder viewHolder, int direction) {}

    @Override
    public void clearView(@NonNull RecyclerView recyclerView, @NonNull RecyclerView.ViewHolder viewHolder) {
        super.clearView(recyclerView, viewHolder);
        if (removed){
            listener.onDragRemove(obsID, old);
        }
        else if (moved){
            gridRecyclerAdapter.swapItem(oldPos[0], newPos[0]);
            listener.onDragMove(obsID, old, newO);
        }
        removed = false;
        moved = false;
    }

    @Override
    public void onChildDraw(@NonNull Canvas c, @NonNull RecyclerView recyclerView, @NonNull RecyclerView.ViewHolder viewHolder, float dX, float dY, int actionState, boolean isCurrentlyActive) {
        int position = viewHolder.getAdapterPosition();
        int xPos = viewHolder.getLayoutPosition() % 21;
        int yPos = viewHolder.getLayoutPosition() / 21;
        float px = (float) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 23, context.getResources().getDisplayMetrics());
        if (position <  0) return;
//        removed = false;
        if (actionState == ItemTouchHelper.ACTION_STATE_DRAG){
            if (dX < -(px * xPos) ||  dX > px*(21-xPos) ||
                    dY < -(px * yPos) || dY > px*(21-yPos)){
//                Toast.makeText(context.getApplicationContext(), position, Toast.LENGTH_SHORT).show();
                System.out.println(position);
                gridRecyclerAdapter.resetCell(position);
                removed = true;

                old[0] = xPos - 1;
                old[1] = 19 - yPos;
            }
        }
        super.onChildDraw(c, recyclerView, viewHolder, dX, dY, actionState, isCurrentlyActive);
    }

}
