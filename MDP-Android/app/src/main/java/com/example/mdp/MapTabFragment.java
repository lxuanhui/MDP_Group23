package com.example.mdp;

import static com.example.mdp.R.*;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.TypedValue;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.ItemTouchHelper;
import androidx.recyclerview.widget.RecyclerView;

import com.example.mdp.arena.Cell;
import com.example.mdp.arena.Directions;
import com.example.mdp.arena.DragListener;
import com.example.mdp.arena.DragSimpleCallback;
import com.example.mdp.arena.GridArena;
import com.example.mdp.arena.OnCellClickListener;
import com.example.mdp.arena.Player;
import com.example.mdp.arena.RecyclerAdapter;

import java.lang.reflect.Array;
import java.util.Arrays;
import java.util.List;

import kotlin.jvm.internal.Ref;

public class MapTabFragment extends Fragment implements OnCellClickListener, DragListener {
    private static final String TAG = "MapFragment";
    private Player carPlayer;

//    SharedPreferences mapPref;

    private SharedViewModel model;
    GridArena arena;
    RecyclerView gridRecyclerView;
    private RecyclerAdapter gridRecyclerAdapter;
    private List<Cell> grid;
    boolean setObstacle = false;
    ImageButton obsBtn, carBtn, carDirBtn;
    Button resetBtn, sendMap;

    Switch dragSwitch;
    int obId=0;
    private boolean setCar = false;



    public MapTabFragment(RecyclerView gridRecyclerView, Player carPlayer){
        this.gridRecyclerView = gridRecyclerView;
        this.carPlayer = carPlayer;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (gridRecyclerAdapter == null){
            arena = new GridArena(20,20);
            grid = arena.getGrid();
            gridRecyclerAdapter = new RecyclerAdapter(grid, this);
            gridRecyclerView.setAdapter(gridRecyclerAdapter);
        }

        model = new ViewModelProvider(requireActivity()).get(SharedViewModel.class);
        model.setMapFragment(this);
        model.setGridRecyclerAdapter(gridRecyclerAdapter);
    }

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {
//        View root = inflater.inflate(R.layout.activity_map_config, container, false);


        View root = inflater.inflate(layout.fragment_map, container, false);

        //Reset
        resetBtn =  root.findViewById(id.resetBtn);
        resetBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                arena = new GridArena(20,20);
                grid = arena.getGrid();
                gridRecyclerAdapter.setGrid(grid);
                carPlayer.getCar().setTranslationX(carPlayer.getStartX());
                carPlayer.getCar().setTranslationY(carPlayer.getStartY());

                carPlayer.getCar().setRotation(0);
                carPlayer.setCarDir(Directions.NORTH);
                carPlayer.setCarCoord(new int[]{1,0});
                obId = 0;

                OnDataPass callback = model.getCallback();
                callback.OnResetMap();

            }
        });

        //Send Map
        sendMap = root.findViewById(R.id.sendMapBtn);
        sendMap.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                OnDataPass callback = model.getCallback();
                callback.OnSendMap();
            }
        });

        //Set Car
        carBtn = root.findViewById(id.carBtn);
        carBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                setCar = true;
                carBtn.setBackground(getResources().getDrawable(drawable.border_black_pressed, null));
                carBtn.setPadding(10,10,10,10);
                carPlayer.getCar().setVisibility(View.INVISIBLE);
                OnDataPass callback = model.getCallback();
                callback.OnSetCar();
            }
        });

        //Set Car Direction
        carDirBtn = root.findViewById(id.carDirBtn);
        carDirBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                LayoutInflater inflater = LayoutInflater.from(getContext());
                View dialogViewCar = inflater.inflate(layout.activity_direction, null);

                Spinner carDirSpinner = dialogViewCar.findViewById(id.carDirSpinner);

                ArrayAdapter<Directions> adapterCarDir =
                        new ArrayAdapter<>(getContext(), android.R.layout.simple_spinner_item, Directions.values());
                adapterCarDir.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                carDirSpinner.setAdapter(adapterCarDir);

                int defCDirIndex = adapterCarDir.getPosition(carPlayer.getCarDir());
                carDirSpinner.setSelection(defCDirIndex);

                AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
                builder.setView(dialogViewCar)
                        .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int id) {
                                // handle selections from the spinners
                                Directions newCarDir = (Directions) carDirSpinner.getSelectedItem();
                                carPlayer.setCarDir(newCarDir);
                                switch (newCarDir){
                                    case NORTH:
                                        carPlayer.getCar().setRotation(0);
                                        break;
                                    case EAST:
                                        carPlayer.getCar().setRotation(90);
                                        break;
                                    case SOUTH:
                                        carPlayer.getCar().setRotation(180);
                                        break;
                                    case WEST:
                                        carPlayer.getCar().setRotation(270);
                                        break;
                                }
                                OnDataPass callback = model.getCallback();
                                callback.OnSetCarDir();
                            }
                        })
                        .setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int id) {
                                // do nothing
                            }
                        });
                AlertDialog alert = builder.create();
                alert.show();

            }
        });


        //Set Obstacle
        obsBtn = root.findViewById(id.obsBtn);
        obsBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                setObstacle = ! setObstacle;
                if (setObstacle) obsBtn.setBackground(getResources().getDrawable(drawable.border_black_pressed, null));
                else obsBtn.setBackground(getResources().getDrawable(drawable.border_black_state, null));
                obsBtn.setPadding(10,10,10,10);
            }
        });

        //Drag
        DragSimpleCallback dragSimpleCallback = new DragSimpleCallback(gridRecyclerAdapter, getContext(), this);
        ItemTouchHelper touchHelper = new ItemTouchHelper(dragSimpleCallback);
        touchHelper.attachToRecyclerView(gridRecyclerView);

        dragSwitch = root.findViewById(id.dragSwitch);
        dragSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                dragSimpleCallback.setDragEnabled(isChecked);
                gridRecyclerAdapter.setLongClick(!isChecked);
                gridRecyclerAdapter.notifyDataSetChanged();
            }
        });

        return root;
    }

    @Override
    public void onCellClick(Cell cell, int position) {
        int r = 19 - position/21;
        int c = position%21 - 1 ;
        float px = TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 23, getResources().getDisplayMetrics());
//        Toast.makeText(getContext(), Integer.toString(position) +" "+ Integer.toString(c)+" "+ Integer.toString(r), Toast.LENGTH_SHORT).show();
        if (setCar && r >= 0 && r < 19 && c > 0 ){
            float X = carPlayer.getStartX();
            float Y = carPlayer.getStartY();
            if (r > 0)
                Y = Y - px * r;
            if (c > 1)
                X = X + px * (c-1);

            if (gridRecyclerAdapter.getCellId(position) > 0 || gridRecyclerAdapter.getCellId(position-1) > 0
            || gridRecyclerAdapter.getCellId(position-21) > 0 || gridRecyclerAdapter.getCellId(position - 21- 1) > 0){
                msg("Cells contain obstacle");
                return;
            }
            carPlayer.getCar().setTranslationY(Y);
            carPlayer.getCar().setTranslationX(X);
            carPlayer.getCar().setRotation(0);
            carPlayer.setCarDir(Directions.NORTH);
            carPlayer.setCarCoord(new int[]{c,r});
            setCar = false;
            carPlayer.getCar().setVisibility(View.VISIBLE);
            carBtn.setBackground(getResources().getDrawable(drawable.border_black_state, null));
            carBtn.setPadding(10,10,10,10);
//            carBtn.setBackgroundColor();
            OnDataPass callback = model.getCallback();
            callback.OnSetCar();
            callback.OnSetCarDir();


//             Toast.makeText(getApplicationContext(),"Car Pos: "+ X+ " , "+ Y, Toast.LENGTH_SHORT).show();
//            msg("Set car at " + Arrays.toString(carPlayer.getCarCoord()));

        }
        else if (setObstacle && r >= 0 && c >= 0) {
            if (cell.getObstacleID() > 0) return;
            if (Arrays.binarySearch(carPlayer.getAllAdapterPos(), position) >= 0) {
                return;
            }
//            System.out.println(Arrays.toString(carPlayer.getAllAdapterPos()));
            obId++;
            cell.setObstacleID(obId);
            gridRecyclerAdapter.setGrid(grid); // Updates the grid displayed on screen
            OnDataPass callback = model.getCallback();
            callback.OnAddObs(obId, new int[]{c,r});
//            Toast.makeText(getContext(),"Obstacle "+ obId +" at: "+ c + " , "+ r, Toast.LENGTH_SHORT).show();

        }


    }

    @Override
    public boolean onCellLongClick(Cell cell, int pos) {
        if (cell.getObstacleID() < 0) return false;

        LayoutInflater inflater = LayoutInflater.from(getContext());
        View dialogView = inflater.inflate(layout.activity_dialog_change_obstacle, null);

        Spinner imgIdSpinner = dialogView.findViewById(id.imgIDSpinner);
        Spinner imgDirSpinner = dialogView.findViewById(id.imgDirSpinner);


        Integer[] imgId_array = new Integer[40 - 11 + 2];
        imgId_array[0] = -1;
        for (int i = 1; i < imgId_array.length; i++) {
            imgId_array[i] = 11 + i - 1;
        }

        ArrayAdapter<Integer> adapterImgId =
                new ArrayAdapter<Integer>(getContext(), android.R.layout.simple_spinner_item, imgId_array){
                    @Override
                    public View getView(int position, View convertView, ViewGroup parent) {
                        View view = super.getView(position, convertView, parent);
                        Integer item = (Integer) getItem(position);
                        if (item != null && item == -1) {
                            ((TextView) view).setText("Null");
                        }
                        return view;
                    }

                    @Override
                    public View getDropDownView(int position, View convertView, ViewGroup parent) {
                        View view = super.getDropDownView(position, convertView, parent);
                        Integer item = getItem(position);
                        if (item != null && item == -1) {
                            ((TextView) view).setText("Null");
                        }
                        return view;
                    }
                };
        adapterImgId.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        imgIdSpinner.setAdapter(adapterImgId);
        Integer cur_imgId = cell.getImgID();
        if (cur_imgId == -1) cur_imgId = null;

        int defIdIndex = adapterImgId.getPosition(cur_imgId);
        imgIdSpinner.setSelection(defIdIndex);


        ArrayAdapter<Directions> adapterImgDir =
                new ArrayAdapter<>(getContext(), android.R.layout.simple_spinner_item, Directions.values());
        adapterImgDir.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        imgDirSpinner.setAdapter(adapterImgDir);
        int defDirIndex = adapterImgDir.getPosition(cell.getImgDir());
        imgDirSpinner.setSelection(defDirIndex);

        AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
        builder.setView(dialogView)
                .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // handle selections from the spinners
                        Integer newImgId = (Integer) imgIdSpinner.getSelectedItem();
                        if (newImgId == null) newImgId = -1;
                        cell.setImgID((int) newImgId);
                        Directions newImgDir = (Directions) imgDirSpinner.getSelectedItem();
                        cell.setImgDir(newImgDir);

                        gridRecyclerAdapter.notifyDataSetChanged();

                        OnDataPass callback = model.getCallback();
                        callback.changeImgDir(cell.getObstacleID(), newImgDir, newImgId);
                    }
                })
                .setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // do nothing
                    }
                });
        AlertDialog alert = builder.create();
        alert.show();


        return false;
    }

    @Override
    public void onDragMove(int obsId, int[] oldPos, int[] newPos) {
        OnDataPass callback = model.getCallback();
        callback.OnObsPass(obsId, oldPos, newPos);
//        msg("Move Obstacle "+ Integer.toString(obsId) + " From " + Arrays.toString(oldPos) + " To " + Arrays.toString(newPos));
    }

    @Override
    public void onDragRemove(int obsId, int[] oldPos) {
        OnDataPass callback = model.getCallback();
        callback.OnObsPass(obsId, oldPos, null);
//        msg("Remove Obstacle "+ Integer.toString(obsId) + " From " + Arrays.toString(oldPos));
    }
    public void msg(String msg){
        Toast.makeText(getContext(), msg, Toast.LENGTH_SHORT).show();
    }
}
