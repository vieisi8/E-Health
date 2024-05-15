package com.example.demo.open_ai;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.example.demo.history._ChatHistory;
import com.example.demo.user.UserService;
import com.example.demo.history.ChatHistory;
import com.example.demo.history.ChatHistroyService;

import jakarta.servlet.http.HttpSession;
import reactor.core.publisher.Mono;

import java.util.List;

@Controller
public class Rest_Api_Controller {

	@Autowired
	private Rest_Api_Service service;
	@Autowired
	private UserService userservice;
	@Autowired
	private ChatHistroyService chathistroysevice;

	@PostMapping("/chatbot")
	public String getJsonData(@RequestParam("Question") String question, Model model, HttpSession session,
			Authentication authentication) {

		// 통신 부분을 호출하여 결과를 받아옴
		DataResponse dataResponse = service.callRemoteAPI(question, session);

		if (dataResponse != null) {
			// 결과를 처리하고 세션, 모델에 정보를 추가
			service.processApiResponse(question, dataResponse, session, model, authentication);
		}

		service.getSidebarContent(model, authentication);

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {
			String id = authentication.getName();
			String name = userservice.getName(id);

			model.addAttribute("name", name);
		}

		// 결과 페이지 반환
		return "main_detail";
	}

	@GetMapping("/chatbot/{code}")
	public String showChatHistory(@PathVariable(value = "code") String code, Model model,
			Authentication authentication) {
		List<ChatHistory> chathistroy = chathistroysevice.getCode(code);

		service.getSidebarContent(model, authentication);

		// 모델에 대화 기록을 추가
		model.addAttribute("chatHistory", chathistroy);

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {
			String id = authentication.getName();
			String name = userservice.getName(id);

			model.addAttribute("name", name);
		}
		return "histroy_detail";

	}

	@PostMapping("/chatbot/{code}")
	public String addChatHistory(@PathVariable(value = "code") String code, @RequestParam("Question") String question,
			HttpSession session, Model model, Authentication authentication) {

		// 현재 코드를 세션에 저장
		session.setAttribute("histroy_code", code);

		model.addAttribute("code", code);

		// 통신 부분을 호출하여 결과를 받아옴
		DataResponse dataResponse = service.callRemoteAPI(question, session);

		if (dataResponse != null) {
			// 결과를 처리하고 세션, 모델에 정보를 추가
			service.histroy_processApiResponse(question, dataResponse, session, authentication);
		}

		List<ChatHistory> chathistroy = chathistroysevice.getCode(code);

		service.getSidebarContent(model, authentication);

		// 모델에 대화 기록을 추가
		model.addAttribute("chatHistory", chathistroy);

		service.getSidebarContent(model, authentication);

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {
			String id = authentication.getName();
			String name = userservice.getName(id);

			model.addAttribute("name", name);
		}
		return "histroy_detail";
	}
	
	@GetMapping("/guide")
	public String guide(Model model, Authentication authentication) {
		
		// 사용자가 로그인 상태인지 확인
				if (authentication != null && authentication.isAuthenticated()) {
					String id = authentication.getName();
					String name = userservice.getName(id);

					model.addAttribute("name", name);
				}
		
		return "guide";
	}
	
	@GetMapping("/how-it-works")
	public String how_it_works(Model model, Authentication authentication) {
		
		// 사용자가 로그인 상태인지 확인
				if (authentication != null && authentication.isAuthenticated()) {
					String id = authentication.getName();
					String name = userservice.getName(id);

					model.addAttribute("name", name);
				}
		
		return "how-it-works";
	}

}
