package com.example.demo.admin;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import com.example.demo.user.UserService;

@Controller
public class AdminController {

	@Autowired
	private AdminService adminservice;
	@Autowired
	private UserService userService;

	@GetMapping("/admin")
	public String showProcessAndError(Model model, Authentication authentication) {

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {
			String id = authentication.getName();
			String name = userService.getName(id);

			model.addAttribute("name", name);
		}

		adminservice.get_process(model, authentication);
		adminservice.get_error_and_prompt(model, authentication);

		return "admin";

	}

}
