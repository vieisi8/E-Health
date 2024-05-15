package com.example.demo;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;
import org.springframework.ui.Model;

@Service
public class MainService {
	private Map<String, List<String>> muscleGroups = new HashMap<>();
	
	void getMuscle_Categories(Model model) {
        // 가슴
        List<String> chestMuscles = new ArrayList<>();
        chestMuscles.add("대흉근");
        chestMuscles.add("상부 대흉근");
        chestMuscles.add("소흉근");
        chestMuscles.add("하부 대흉근");
        muscleGroups.put("가슴", chestMuscles);

        // 어깨
        List<String> shoulderMuscles = new ArrayList<>();
        shoulderMuscles.add("후면 삼각근");
        shoulderMuscles.add("극하근");
        shoulderMuscles.add("전면 삼각근");
        shoulderMuscles.add("측면 삼각근");
        muscleGroups.put("어깨", shoulderMuscles);

        // 팔
        List<String> armMuscles = new ArrayList<>();
        armMuscles.add("상완 이두근");
        armMuscles.add("상완 삼두근");
        armMuscles.add("장두");
        armMuscles.add("상완근");
        armMuscles.add("상완 요골근");
        armMuscles.add("손목 굴곡근");
        armMuscles.add("손목 신근");
        armMuscles.add("회내근");
        armMuscles.add("회외근");
        muscleGroups.put("팔", armMuscles);

        // 복근
        List<String> abdominalMuscles = new ArrayList<>();
        abdominalMuscles.add("복직근");
        abdominalMuscles.add("내복사근");
        abdominalMuscles.add("외복사근");
        muscleGroups.put("복근", abdominalMuscles);

        // 등
        List<String> backMuscles = new ArrayList<>();
        backMuscles.add("광배근");
        backMuscles.add("대원근");
        backMuscles.add("중하부 승모근");
        backMuscles.add("능형근");
        backMuscles.add("척추 기립근");
        backMuscles.add("등 전체");
        backMuscles.add("상부 승모근");
        backMuscles.add("뒷면");
        backMuscles.add("전거근");
        muscleGroups.put("등", backMuscles);

        // 하체
        List<String> legMuscles = new ArrayList<>();
        legMuscles.add("대둔근");
        legMuscles.add("장요근");
        legMuscles.add("가자미근");
        legMuscles.add("고관절 외전근");
        legMuscles.add("대내전근");
        legMuscles.add("장내전근");
        legMuscles.add("단내전근");
        legMuscles.add("대퇴근막장근");
        legMuscles.add("중둔근");
        legMuscles.add("소둔근");
        legMuscles.add("대퇴 사두근");
        legMuscles.add("비복근");
        legMuscles.add("햄스트링");
        legMuscles.add("슬건근");
        muscleGroups.put("하체", legMuscles);

        // 목
        List<String> neckMuscles = new ArrayList<>();
        neckMuscles.add("흉쇄유돌근");
        muscleGroups.put("목", neckMuscles);
        
        model.addAttribute("Muscle_Categories", muscleGroups);
	}

}
