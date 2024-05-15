package com.example.demo.recommended_exercise;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.ui.Model;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class RecommendedexerciseService {

	@Autowired
	private RecommendedexerciseRepository recommendedexerciseRepository;

	private static final Map<String, List<String>> TAGS_MAP = new HashMap<>();

	static {
		TAGS_MAP.put("등", Arrays.asList("광배근", "광배근", "대원근", "중하부 승모근", "능형근", "척추 기립근", "등 전체", "상부 승모근", "뒷면",
				"작은 원근", "작은원근", "전거근", "척추 기립"));
		TAGS_MAP.put("가슴", Arrays.asList("흉골(하부) 대흉근", "대흉근", "상부 대흉근", "소흉근", "쇄골(상부) 가슴", "하부 대흉근"));
		TAGS_MAP.put("어깨", Arrays.asList("후면 삼각근", "극하근", "전면 삼각근", "외측 삼각근", "전면 삼각근", "측면 삼각근"));
		TAGS_MAP.put("팔",
				Arrays.asList("상완 이두근", "상완 삼두근", "장두", "상완근", "상완 요골근", "상완요골근", "손목 굴곡근", "손목 신근", "회내근", "회외근"));
		TAGS_MAP.put("복근", Arrays.asList("복직근", "내부 복사근", "외부 복사근", "내복사근", "외복사근"));
		TAGS_MAP.put("하체", Arrays.asList("대둔근", "장요근", "가자미근", "고관절 외전근", "대내전근", "장내전근", "단내전근", "대퇴근막장근", "중둔근",
				"소둔근", "대퇴 사두근", "대퇴사두근", "비복근", "햄스트링", "슬건근"));
		TAGS_MAP.put("목", Arrays.asList("흉쇄유돌근"));
		TAGS_MAP.put("없음", Arrays.asList("없음"));
	}
	
	private List<String> tags = new ArrayList<>();
	

	public List<Recommended_exercise> getRandomExercises(Model model) {
		
		List<Recommended_exercise> allExercises = recommendedexerciseRepository.findAll();
		
		getTag();

		for(int i=0; i<allExercises.size(); i++) {
			Recommended_exercise exercise = allExercises.get(i);
			String tag = tags.get(i);
			
			exercise.setTag(tag);
			this.recommendedexerciseRepository.save(exercise);
		}

		List<String>tag=Arrays.asList("가슴", "등", "어깨", "팔", "복근", "하체", "목");
		
		// 리스트를 섞음
		Collections.shuffle(tag);
		
		String recommendedTag = tag.get(0);
		
		model.addAttribute("tag", recommendedTag);
		

		List<Recommended_exercise> recommendedExercise = recommendedexerciseRepository.findByTag(recommendedTag);
		
		// 리스트를 섞음
		Collections.shuffle(recommendedExercise);
		// 처음 4개의 요소 선택
		
		int endIndex = Math.min(recommendedExercise.size(), 4);
		
		return recommendedExercise.subList(0, endIndex);
	}

	public void getTag() {

		List<String> type = recommendedexerciseRepository.findAllTypes();
		
		for (String muscle : type) {
			String tag = getTagForType(muscle);
			tags.add(tag);
		}
	}

	private static String getTagForType(String muscle) {
		for (Map.Entry<String, List<String>> entry : TAGS_MAP.entrySet()) {
			String tag = entry.getKey();
			List<String> musclesWithTag = entry.getValue();
			for (String muscleWithTag : musclesWithTag) {

				// 예외 처리
				if (muscle.equals("광배근, 복직근")) {
					return "등";
				} else if (muscle.equals("광배근, 흉골(하부) 대흉근, 복직근")) {
					return "등";
				} else if (muscle.equals("대둔근, 척추 기립근")) {
					return "하체";
				} else if (muscle.equals("대퇴사두근(대퇴직근, 외측광근, 중간광근, 내측광근), 상완 이두근")) {
					return "하체";
				} else if (muscle.equals("대퇴사두근, 복직근")) {
					return "하체";
				} else if (muscle.equals("상완 삼두근, 대둔근, 대퇴사두근")) {
					return "하체";
				} else if (muscle.equals("일반적으로 등")) {
					return "등";
				} else if (muscle.equals("장요근. 안정근인 복직근도 목표 근육으로 볼 수 있습니다.")) {
					return "하체";
				} else if (muscle.equals("장요근. 중요한 안정근인 복직근도 목표 근육으로 볼 수 있습니다.")) {
					return "하체";
				} else if (muscle.equals("척추 기립근, 햄스트링")) {
					return "하체";
				} else if (muscle.equals("하부 대흉근, 복직근")) {
					return "가슴";
				} else if (muscle.equals("흉골(하부) 대흉근, 장요근, 외복사근")) {
					return "가슴";
				} else {
					// 주어진 문자열에 해당하는 근육이 목록에 포함되어 있는지 확인
					if (muscle.contains(muscleWithTag)) {
						return tag; // 발견되면 해당 태그 반환
					}

				}
			}
		}
		return "없음";
	}
}
