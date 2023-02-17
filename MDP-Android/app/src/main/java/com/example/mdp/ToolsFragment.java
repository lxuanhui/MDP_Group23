package com.example.mdp;

//import android.os.Bundle;
//import android.view.LayoutInflater;
//import android.view.View;
//import android.view.ViewGroup;
//
//import androidx.fragment.app.Fragment;
//import androidx.viewpager2.adapter.FragmentStateAdapter;
//import androidx.viewpager2.widget.ViewPager2;
//
//public class ToolsFragment extends Fragment {
//
//    @Override
//    public View onCreateView(LayoutInflater inflater, ViewGroup container,
//                             Bundle savedInstanceState) {
//        View view = inflater.inflate(R.layout.fragment_tools, container, false);
//        ViewPager2 viewPager = view.findViewById(R.id.pager);
//        viewPager.setAdapter(new MyFragmentStateAdapter(this));
//        return view;
//    }
//
//    private static class MyFragmentStateAdapter extends FragmentStateAdapter {
//
//        MyFragmentStateAdapter(Fragment fragment) {
//            super(fragment);
//        }
//
////        @NonNull
//        @Override
//        public Fragment createFragment(int position) {
//            switch (position) {
//                case 0:
////                    return new FragmentOne();
//                    return null;
//                case 1:
//                    return new MapTabFragment();
//                case 2:
////                    return new FragmentThree();
//                    return null;
//                default:
////                    return new FragmentOne();
//                    return null;
//            }
//        }
//
//        @Override
//        public int getItemCount() {
//            return 3;
//        }
//    }
//}
