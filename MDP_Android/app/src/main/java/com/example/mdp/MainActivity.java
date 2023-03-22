package com.example.mdp;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.IntentFilter;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.util.TypedValue;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.viewpager2.widget.ViewPager2;

import com.example.mdp.bluetooth.BluetoothFragment;
import com.example.mdp.bluetooth.OnBluetoothReadReceivedListener;
import com.example.mdp.bluetooth.OnBluetoothStateChangedListener;
import com.example.mdp.bluetooth.receivers.BluetoothConnectionStateBroadcastReceiver;
import com.example.mdp.bluetooth.receivers.BluetoothScanBroadcastReceiver;
import com.example.mdp.bluetooth.receivers.BluetoothStateBroadcastReceiver;
import com.example.mdp.bluetooth.service.BluetoothService;
import com.example.mdp.databinding.ActivityMainBinding;

import com.example.mdp.arena.*;
import com.example.mdp.timer.TimerFragment;
import com.google.android.material.tabs.TabLayout;
import com.google.android.material.tabs.TabLayoutMediator;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.Arrays;


public class MainActivity extends AppCompatActivity implements  OnDataPass, OnRemoteClickListener {
    // Bluetooth
    private AppBarConfiguration appBarConfiguration;

    //Arena
    RecyclerView gridRecyclerView;
    RecyclerAdapter gridRecyclerAdapter = null;
    GridArena arena;
    // Controller
    ImageButton up, down, left, right;

    //Car
    Player carPlayer;
    ImageView car;
    Directions carDir;
    int[] carCoord = new int[2];
    TextView carDirText, carXText, carYText;
    static TextView robotStatus;
    int[][] obstacles = new int[20][4];
    //obstacle[obsid] = [obsid, x, y, imgdir]


    //Reset
    ImageButton reset;
    private SharedViewModel model;

    //Timer
    final Handler handler = new Handler();
    private static final String TAG = "Main Activity";
    public static boolean stopTimerFlag = false;
    public static boolean stopWk9TimerFlag = false;

    private BluetoothService bluetoothService;
    private OnBluetoothReadReceivedListener chatReadListener;

    private BluetoothConnectionStateBroadcastReceiver connectionStateBroadcastReceiver;
    private BluetoothScanBroadcastReceiver scanBroadcastReceiver;
    private BluetoothStateBroadcastReceiver stateBroadcastReceiver;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
//        setContentView(R.layout.activity_main);

        com.example.mdp.databinding.ActivityMainBinding binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        setSupportActionBar(binding.toolbar);
        getSupportActionBar().setTitle(R.string.app_name);

        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        appBarConfiguration = new AppBarConfiguration.Builder(navController.getGraph()).build();
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);


        //VieModel
        model = new ViewModelProvider(this).get(SharedViewModel.class);
        model.setCallback(this);

        //Arena
        gridRecyclerView = findViewById(R.id.ArenaRecycler);
//        GridLayoutManager gridLayoutManager = new GridLayoutManager(this, 21);
//        gridLayoutManager.setSpanSizeLookup(new GridLayoutManager.SpanSizeLookup() {
//            @Override
//            public int getSpanSize(int position) {
//                return 1;
//            }
//        });
//        gridRecyclerView.setLayoutManager(gridLayoutManager);
        gridRecyclerView.setLayoutManager(new GridLayoutManager(this, 21));
        arena = new GridArena(20,20);
//        gridRecyclerAdapter = null;

        // Car
        car = findViewById(R.id.Car);
        carPlayer = new Player(car, car.getTranslationX(), car.getTranslationY());
        carDirText = findViewById(R.id.directionAxisTextView);
        carXText = findViewById(R.id.xAxisTextView);
        carYText = findViewById(R.id.yAxisTextView);
        robotStatus = findViewById(R.id.robotStatus);

        //Initialize the ViewPager2 and TabLayout
        ViewPager2 viewPager = findViewById(R.id.pager);
        viewPager.setAdapter(new MyFragmentStateAdapter(this, gridRecyclerView, gridRecyclerAdapter, arena.getGrid(), carPlayer));
        viewPager.setOffscreenPageLimit(2);
        TabLayout tabLayout = findViewById(R.id.tabs);

        // Attach the TabLayout to the ViewPager2 using the TabLayoutMediator
        String[] tabNames = { "Map", "Chat", "Timer"};
        new TabLayoutMediator(tabLayout, viewPager,
                (tab, position) -> tab.setText(tabNames[position])).attach();

        // Controller
        up = findViewById(R.id.Up);
        down = findViewById(R.id.Down);
        left = findViewById(R.id.Left);
        right = findViewById(R.id.Right);
        // TODO Check for obstacles
        // TODO Check if player on Arena moving right on actual Device
        // TODO Command to move Robo
        down.setOnClickListener((view) -> OnDownClickListener());
        up.setOnClickListener((view) -> OnUpClickListener());
        right.setOnClickListener((view) -> OnRightClickListener());
        left.setOnClickListener((view) -> OnLeftClickListener());

        TextView bluetoothStatus2 = findViewById(R.id.bluetoothStatus2);
        TextView bluetoothConnectedDevice = findViewById(R.id.bluetoothConnectedDevice);

        OnBluetoothReadReceivedListener onBluetoothReadReceivedListener = message -> {
            runOnUiThread(() -> {
                if (message.contains("robotPosition")) {
                    try {
                        JSONObject json = new JSONObject(message);
                        JSONArray position = json.getJSONArray("robotPosition");
                        int x = position.getInt(0);
                        int y = position.getInt(1);
                        int deg = position.getInt(2);
                        updateCar(x, y, deg); // car Movement
                        carXText.setText(String.valueOf(x));
                        carYText.setText(String.valueOf(y));
                        switch (deg) {
                            case 0:
                                carDirText.setText("NORTH");
                                break;

                            case 90:
                                carDirText.setText("EAST");
                                break;

                            case 180:
                                carDirText.setText("SOUTH");
                                break;

                            case 270:
                                carDirText.setText("WEST");
                                break;
                        }
                        // todo map.update(x, y, deg);
                    } catch (JSONException e) {
                        // throw new RuntimeException(e);
                    }
                }
                if (message.contains("status")) {
                    try {
                        JSONObject json = new JSONObject(message);
                        String status = json.getString("status");
                        robotStatus.setText(status);
                    } catch (JSONException e) {
                        // throw new RuntimeException(e);
                    }
                }
                if (message.contains("target")) {
                    try {
                        JSONObject json = new JSONObject(message);
                        JSONArray target = json.getJSONArray("target");
                        int obsID = target.getInt(0);
                        int imgId = target.getInt(1);
                        changeImgId(obsID, imgId);
                    } catch (JSONException e) {
                        // throw new RuntimeException(e);
                    }
                }
                else if (message.equals("End Challenge")) {
                    // if wk 8 btn is checked, means running wk 8 challenge and likewise for wk 9
                    // end the corresponding timer
                    ToggleButton exploreButton = findViewById(R.id.exploreToggleBtn2);
                    ToggleButton fastestButton = findViewById(R.id.fastestToggleBtn2);

                    if (exploreButton.isChecked()) {
                        showLog("explorebutton is checked");
                        stopTimerFlag = true;
                        exploreButton.setChecked(false);
                        robotStatus.setText("Auto Movement/ImageRecog Stopped");
                        TimerFragment.timerHandler.removeCallbacks(TimerFragment.timerRunnableExplore);
                    } else if (fastestButton.isChecked()) {
                        showLog("fastestbutton is checked");
                        stopTimerFlag = true;
                        fastestButton.setChecked(false);
                        robotStatus.setText("Week 9 Stopped");
                        TimerFragment.timerHandler.removeCallbacks(TimerFragment.timerRunnableFastest);
                    }
                }
                chatReadListener.onBluetoothReadReceived(message);
            });
        };
        AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(this);
        alertDialogBuilder.setTitle("Reconnecting");
        alertDialogBuilder.setMessage("Reconnecting to device...").setCancelable(false);
        AlertDialog alertDialog = alertDialogBuilder.create();
        OnBluetoothStateChangedListener onBluetoothStateChangedListener = new OnBluetoothStateChangedListener() {
            @Override
            public void onDisconnect() {
                runOnUiThread(() -> {
                    bluetoothStatus2.setText("Not Connected");
                    bluetoothConnectedDevice.setText("");
                    if (bluetoothService.canReconnect()) {
                        alertDialog.show();
                        bluetoothService.reconnect();
                    }
                });
            }

            @SuppressLint("MissingPermission")
            @Override
            public void onConnect(BluetoothDevice bluetoothDevice) {
                runOnUiThread(() -> {
                    bluetoothStatus2.setText("Connected");
                    String deviceName = bluetoothService.getDevice().getName();
                    bluetoothConnectedDevice.setText(deviceName);
                    Toast.makeText(MainActivity.this, "Connected to " + deviceName, Toast.LENGTH_SHORT).show();
                    alertDialog.dismiss();
                });
            }
        };
        bluetoothService = new BluetoothService(onBluetoothReadReceivedListener, onBluetoothStateChangedListener);
        registerReceivers();
    }

    @Override
    public boolean onSupportNavigateUp() {
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        return NavigationUI.navigateUp(navController, appBarConfiguration) || super.onSupportNavigateUp();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            // do nothing for now
            return true;
        } else if (id == R.id.action_bluetooth) {
            // Navigation.findNavController(this, R.id.nav_host_fragment_content_main).navigate(R.id.action_MainFragment_to_BluetoothFragment);
            new BluetoothFragment(bluetoothService).show(getSupportFragmentManager(), "BluetoothFragment");
        }
        return super.onOptionsItemSelected(item);
    }

    // BLUETOOTH
    private void registerReceivers() {
        scanBroadcastReceiver = new BluetoothScanBroadcastReceiver();
        registerReceiver(scanBroadcastReceiver, new IntentFilter(BluetoothAdapter.ACTION_SCAN_MODE_CHANGED));

        stateBroadcastReceiver = new BluetoothStateBroadcastReceiver();
        registerReceiver(stateBroadcastReceiver, new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED));

        connectionStateBroadcastReceiver = new BluetoothConnectionStateBroadcastReceiver();
        registerReceiver(connectionStateBroadcastReceiver, new IntentFilter(BluetoothAdapter.ACTION_CONNECTION_STATE_CHANGED));
    }
    // Timer
    public static TextView getRobotStatusTextView(){
        return robotStatus;
    };
    private static void showLog(String message) {
        Log.d(TAG, message);
    }
//    public static void printMessage(String message){
//        bluetoothService.write(message);
//    }

    // ARENA

    public void msg(String msg){
        Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
        // Send message to car via bluetooth - TODO
        //bluetoothService.write(msg + "\n");
    }

    public void changeImgId(int obsId, int newImgId){
//        obstacles[obsId][3] = newImgId;
//        model.setObstacles(obstacles);

        int[] pos = new int[]{obstacles[obsId][1], obstacles[obsId][2]};
        setImgId(newImgId, pos);

    }
    public void setImgId(int imgId, int[] pos){
        int layoutpos = (19 - pos[1]) * 21 + (pos[0] + 1);
        gridRecyclerAdapter = model.getGridRecyclerAdapter();
        gridRecyclerAdapter.setImgId(imgId, layoutpos);

    }

    // Map Fragment
    @Override
    public void OnObsPass(int obsId, int[] oldPos, int[] newPos){
        if (newPos == null){
            obstacles[obsId] = new int[4];
            model.setObstacles(obstacles);
            msg("Remove Obstacle "+ Integer.toString(obsId) + " From " + Arrays.toString(oldPos));
//            bluetoothService.write("Remove Obstacle "+ Integer.toString(obsId) + " From " + Arrays.toString(oldPos) + "\n");
        }
        else {
            obstacles[obsId][1] = newPos[0];
            obstacles[obsId][2] = newPos[1];
            model.setObstacles(obstacles);
            msg("Move Obstacle " + Integer.toString(obsId) + " From " + Arrays.toString(oldPos) + " To " + Arrays.toString(newPos));
//            bluetoothService.write("Move Obstacle " + Integer.toString(obsId) + " From " + Arrays.toString(oldPos) + " To " + Arrays.toString(newPos)+ "\n");
        }
    }

    @Override
    public void OnAddObs(int obsId, int[] pos) {
        obstacles[obsId] = new int[]{obsId, pos[0], pos[1], 90};
        model.setObstacles(obstacles);
        msg("Add Obstacle " + Integer.toString(obsId) + " At " + Arrays.toString(pos));
//        if (obsId == 3) {
//            changeImgId(3, 34);
//        }
//        bluetoothService.write("Obstacle " + Integer.toString(obsId) + ", " + Arrays.toString(pos) + "\n");
    }
    @Override
    public void changeImgDir(int obsId, Directions newImgDir, int newImgId) {
        switch (newImgDir){
            case NORTH:
                obstacles[obsId][3] = 0;
                break;
            case EAST:
                obstacles[obsId][3] = 90;
                break;
            case SOUTH:
                obstacles[obsId][3] = 180;
                break;
            case WEST:
                obstacles[obsId][3] = 270;
                break;
        }
//        obstacles[obsId][4] = newImgId; //todo check if needed
//        model.setObstacles(obstacles);

    }

    @Override
    public void OnSendMap() {
        System.out.println("================");
//        carCoord = carPlayer.getCarCoord();
//        carDir = carPlayer.getCarDir();
//
//        bluetoothService.write("car" + Integer.toString(carCoord[0]) + ", "
//                + Integer.toString(carCoord[1])+ ", "+ carDir.toString() +"\n");

        for (int i=0; i<20; i++){
            int[] obsInfo = obstacles[i];
            if (obsInfo[0] > 0){
                int obsidm = obsInfo[0];
                int[] obsCoordm = new int[]{obsInfo[1], obsInfo[2]};
                String imgDirm = "NIL";
                switch (obsInfo[3]){
                    case(0):
                        imgDirm = "N";
                        break;
                    case(90):
                        imgDirm = "E";
                        break;
                    case(180):
                        imgDirm = "S";
                        break;
                    case(270):
                        imgDirm = "W";
                        break;
                }
                String ObsMsgString = Integer.toString(obsidm) + ", " + Arrays.toString(obsCoordm) + ", " + imgDirm;
<<<<<<< HEAD
                bluetoothService.write("obstacle ["+ObsMsgString+"]"); // String msg: obstacle [<obsid> , [<x> , <y>], <imgdir>]
//                bluetoothService.write( "obstacle "+ Arrays.toString(obsInfo) +"\n"); // String msg: obstacle [<obsid> , <x> , <y>, <imgdir>]


                System.out.println("obstacle ["+ObsMsgString+"]");
=======
                bluetoothService.write("{\"obstacle\" ["+ObsMsgString+"]}"); // String msg: {"obstacle": [<obsid> , [<x> , <y>], <imgdir>]}
//                bluetoothService.write( "obstacle "+ Arrays.toString(obsInfo) +"\n"); // String msg: obstacle [<obsid> , <x> , <y>, <imgdir>]


                System.out.println("{\"obstacle\": ["+ObsMsgString+"]}");
>>>>>>> 83b415ac926812d70846481ae999da5c8fbef8e3
            }
            // put x, y coord in a tuple
            // send directions as , N,S, W,E
        }
        System.out.println("================");
    }

    @Override
    public void OnSetCar() {
        car = carPlayer.getCar();
        carDir = carPlayer.getCarDir();
        carCoord = carPlayer.getCarCoord();
        msg("Set car at " + Arrays.toString(carPlayer.getCarCoord()));
//        bluetoothService.write("Set car at " + Arrays.toString(carPlayer.getCarCoord())+ "\n");
//        bluetoothService.write("car" + Integer.toString(carCoord[0]) + ", "
//                + Integer.toString(carCoord[1])+ ", "+ carDir.toString() +"\n");
        carXText.setText(Integer.toString(carCoord[0]));
        carYText.setText(Integer.toString(carCoord[1]));
    }

    @Override
    public void OnSetCarDir() {
//        changeImgId(3, 34); // sets on 2 click, first click toggles


        car = carPlayer.getCar();
        carCoord = carPlayer.getCarCoord();
        carDir = carPlayer.getCarDir();
        msg("Set car direction to " + carDir);
//        bluetoothService.write("Set car direction to " + carDir + "\n");
//        bluetoothService.write("car" + Integer.toString(carCoord[0]) + ", " + Integer.toString(carCoord[1])+ ", "+ carDir.toString() +"\n");
        carDirText.setText(carDir.toString());

    }

    @Override
    public void OnResetMap() {
        obstacles = new int[20][4];
        car = carPlayer.getCar();
        carCoord = carPlayer.getCarCoord();
        carDir = carPlayer.getCarDir();
        gridRecyclerAdapter = model.getGridRecyclerAdapter();
        msg("Reset map");
        bluetoothService.write("Reset");
        carXText.setText(Integer.toString(carCoord[0]));
        carYText.setText(Integer.toString(carCoord[1]));
        carDirText.setText(carDir.toString());

    }

    // Map update
    public void updateCar(int x, int y, int carDeg){
        float px = TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 23, getResources().getDisplayMetrics());
        float X = carPlayer.getStartX();
        float Y = carPlayer.getStartY();
        if (y > 0)
            Y = Y - px * y;
        if (x > 1)
            X = X + px * (x-1);

        if (carDeg == 0 || carDeg == 180) //North, South
        {
            carPlayer.getCar().animate().translationY(Y);
            carPlayer.getCar().animate().rotation(carDeg);
            carPlayer.getCar().animate().translationX(X);

        }
        else{
            carPlayer.getCar().animate().translationY(Y);
            carPlayer.getCar().animate().rotation(carDeg);
            carPlayer.getCar().animate().translationX(X);
        }


    }
    // Controller
    @Override
    public void OnUpClickListener() {
//        float px = TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 23, getResources().getDisplayMetrics());
//        carCoord = carPlayer.getCarCoord();
//        carDir = carPlayer.getCarDir();
//        gridRecyclerAdapter = model.getGridRecyclerAdapter();
//
//        switch (carDir) {
//            case NORTH:
//                if (carCoord[1] >= 0 && carCoord[1] < 19 &&
//                        !gridRecyclerAdapter.isObstacle(carCoord[0], carCoord[1] + 2) &&
//                        !gridRecyclerAdapter.isObstacle(carCoord[0] - 1, carCoord[1] + 2)) {
//
//                    carPlayer.getCar().animate().translationYBy(-px);
//                    carCoord[1] = carCoord[1] + 1;
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move up to " + Arrays.toString(carCoord));
//                }
//                break;
//            case SOUTH:
//                if (carCoord[1] > 0) {
//                    carPlayer.getCar().animate().translationYBy(px);
//                    carCoord[1] = carCoord[1] - 1;
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move up to " + Arrays.toString(carCoord));
//                }
//                break;
//            case EAST:
//                if (carCoord[0] < 19) {
//                    carPlayer.getCar().animate().translationXBy(px);
//                    carCoord[0] = carCoord[0] + 1;
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move up to " + Arrays.toString(carCoord));
//                    //Move Robo
//                }
//                break;
//            case WEST:
//                if (carCoord[0] > 1) {
//                    carPlayer.getCar().animate().translationXBy(-px);
//                    carCoord[0] = carCoord[0] - 1;
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move up to " + Arrays.toString(carCoord));
//                }
//                break;
//        }
//        carXText.setText(Integer.toString(carCoord[0]));
//        carYText.setText(Integer.toString(carCoord[1]));

        bluetoothService.write("w");
    }

    @Override
    public void OnDownClickListener() {
//        float px = TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 23, getResources().getDisplayMetrics());
//        carCoord = carPlayer.getCarCoord();
//        carDir = carPlayer.getCarDir();
//
//        switch (carDir){
//            case NORTH:
//                if (carCoord[1] > 0) {
//                    carPlayer.getCar().animate().translationYBy((float) 30.61875);
//                    carCoord[1] = carCoord[1] - 1;
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move down to " + Arrays.toString(carCoord));
//                }
//                break;
//            case SOUTH:
//                if (carCoord[1] < 18) {
//                    carPlayer.getCar().animate().translationYBy((float) -30.61875);
//                    carCoord[1] = carCoord[1] + 1;
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move down to " + Arrays.toString(carCoord));
//                }
//                break;
//            case EAST:
//                if (carCoord[0] > 1) {
//                    carPlayer.getCar().animate().translationXBy((float) -30.61875);
//                    carCoord[0] = carCoord[0] - 1;
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move down to " + Arrays.toString(carCoord));
//                }
//                break;
//            case WEST:
//                if (carCoord[0] < 19) {
//                    carPlayer.getCar().animate().translationXBy((float) 30.61875);
//                    carCoord[0] = carCoord[0] + 1;
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move down to " + Arrays.toString(carCoord));
//                }
//                break;
//        }
//        carXText.setText(Integer.toString(carCoord[0]));
//        carYText.setText(Integer.toString(carCoord[1]));

        bluetoothService.write("s");
    }

    @Override
    public void OnLeftClickListener() {
//        float px = TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 23, getResources().getDisplayMetrics());
//        carCoord = carPlayer.getCarCoord();
//        carDir = carPlayer.getCarDir();
//        switch (carDir){
//            case NORTH:
//                if (carCoord[1] > 0  && carCoord[0] < 19) {
//                    carPlayer.getCar().animate().translationYBy(-px);
//                    carPlayer.getCar().animate().rotationBy(-90).setDuration(500).start();
//                    carPlayer.getCar().animate().translationXBy(-px);
//
//                    carDir = Directions.WEST;
//                    carCoord[0] = carCoord[0] - 1;
//                    carCoord[1] = carCoord[1] + 1;
//                }
//                break;
//            case WEST:
//                if (carCoord[0]> 1 && carCoord[1] > 1 ) {
//                    carPlayer.getCar().animate().translationYBy(px);
//                    carPlayer.getCar().animate().rotationBy(-90).setDuration(500).start();
//                    carPlayer.getCar().animate().translationXBy(-px);
//
//                    carDir = Directions.SOUTH;
//                    carCoord[0] = carCoord[0] - 1;
//                    carCoord[1] = carCoord[1] - 1;
//                }
//                break;
//            case SOUTH:
//                if (carCoord[1] > 1 && carCoord[0] < 19){
//                    carPlayer.getCar().animate().translationXBy(px);
//                    carPlayer.getCar().animate().rotationBy(-90).setDuration(500).start();
//                    carPlayer.getCar().animate().translationYBy(px);
//
//                    carDir = Directions.EAST;
//                    carCoord[0] = carCoord[0] + 1;
//                    carCoord[1] = carCoord[1] - 1;
//                }
//                break;
//            case EAST:
//                if (carCoord[0] < 19 && carCoord[1] < 19) {
//                    carPlayer.getCar().animate().translationYBy(-px);
//                    carPlayer.getCar().animate().rotationBy(-90).setDuration(500).start();
//                    carPlayer.getCar().animate().translationXBy(px);
//
//                    carDir = Directions.NORTH;
//                    carCoord[0] = carCoord[0] + 1;
//                    carCoord[1] = carCoord[1] + 1;
//                }
//                break;
//
//        }
//        carPlayer.setCarDir(carDir);
//        carPlayer.setCarCoord(carCoord);
//        msg("move left to " + Arrays.toString(carCoord));

//        carXText.setText(Integer.toString(carCoord[0]));
//        carYText.setText(Integer.toString(carCoord[1]));
//        carDirText.setText(carDir.toString());

        bluetoothService.write("a");
    }

    @Override
    public void OnRightClickListener() {
//        float px = TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 23, getResources().getDisplayMetrics());
//        carCoord = carPlayer.getCarCoord();
//        carDir = carPlayer.getCarDir();
//
//        switch (carDir){
//            case NORTH:
//                if (carCoord[1] >=0  && carCoord[0] < 19) {
//                    carPlayer.getCar().animate().translationYBy(-px);
//                    carPlayer.getCar().animate().rotationBy(90).setDuration(500).start();
//                    carPlayer.getCar().animate().translationXBy(px);
//
//                    carDir = Directions.EAST;
//                    carCoord[0] = carCoord[0] + 1;
//                    carCoord[1] = carCoord[1] + 1;
//
//                    carPlayer.setCarDir(carDir);
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move right to " + Arrays.toString(carCoord));
//                }
//                break;
//            case EAST:
//                if (carCoord[0] < 19 && carCoord[1] < 19) {
//                    carPlayer.getCar().animate().translationXBy(px);
//                    carPlayer.getCar().animate().rotationBy(90).setDuration(500).start();
//                    carPlayer.getCar().animate().translationYBy(px);
//
//                    carDir = Directions.SOUTH;
//                    carCoord[0] = carCoord[0] + 1;
//                    carCoord[1] = carCoord[1] - 1;
//
//                    carPlayer.setCarDir(carDir);
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move right to " + Arrays.toString(carCoord));
//                }
//                break;
//            case SOUTH:
//                if (carCoord[0] > 0 && carCoord[1] >0){
//                    carPlayer.getCar().animate().translationYBy(px);
//                    carPlayer.getCar().animate().rotationBy(90).setDuration(500).start();
//                    carPlayer.getCar().animate().translationXBy(-px);
//
//                    carDir = Directions.WEST;
//                    carCoord[0] = carCoord[0] - 1;
//                    carCoord[1] = carCoord[1] - 1;
//
//                    carPlayer.setCarDir(carDir);
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move right to " + Arrays.toString(carCoord));
//                }
//                break;
//            case WEST:
//                if (carCoord[0] >1 && carCoord[1] < 18){
//                    carPlayer.getCar().animate().translationXBy(-px);
//                    carPlayer.getCar().animate().rotationBy(90).setDuration(500).start();
//                    carPlayer.getCar().animate().translationYBy(-px);
//
//                    carDir = Directions.NORTH;
//                    carCoord[0] = carCoord[0] - 1;
//                    carCoord[1] = carCoord[1] + 1;
//
//                    carPlayer.setCarDir(carDir);
//                    carPlayer.setCarCoord(carCoord);
//                    msg("move right to " + Arrays.toString(carCoord));
//                }
//                break;
//
//        }
//        carXText.setText(Integer.toString(carCoord[0]));
//        carYText.setText(Integer.toString(carCoord[1]));
//        carDirText.setText(carDir.toString());

        bluetoothService.write("d");
    }

    public BluetoothService getBluetoothService() {
        return bluetoothService;
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (bluetoothService != null) {
            bluetoothService.stop();
        }
    }

    public void setChatReadListener(OnBluetoothReadReceivedListener listener) {
        this.chatReadListener = listener;
    }
}
