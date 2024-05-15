package com.example.demo;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import com.example.demo.open_ai.Rest_Api_Service;
import com.example.demo.user.UserService;
import com.example.demo.history.ChatHistroyService;
import com.example.demo.recommended_exercise.Recommended_exercise;
import com.example.demo.recommended_exercise.RecommendedexerciseService;

import jakarta.servlet.http.HttpSession;

@Controller
public class MainController {
	@Autowired
	private Rest_Api_Service service;
	@Autowired
	private UserService userservice;
	@Autowired
	private RecommendedexerciseService recommendedexerciseserive;
	@Autowired
	private MainService mainservice;

	@GetMapping("/")
	public String root(Model model, HttpSession session, Authentication authentication) {
		session.setAttribute("session", "off");

		service.getSidebarContent(model, authentication);

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {
			String id = authentication.getName();
			String name = userservice.getName(id);

			model.addAttribute("name", name);
		}

		String code = ChatHistroyService.generateCode();
		// 현재 코드를 세션에 저장
		session.setAttribute("code", code);
		
		List<Recommended_exercise> recommended_exercise = recommendedexerciseserive.getRandomExercises(model);

		model.addAttribute("recommended_exercise", recommended_exercise);

		
		mainservice.getMuscle_Categories(model);
		
		return "main";
	}
}
