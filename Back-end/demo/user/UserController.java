package com.example.demo.user;

import jakarta.validation.Valid;

import java.util.UUID;

import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.example.demo.from.*;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Controller
@RequestMapping("/user")
public class UserController {

	private final UserService userService;

	@GetMapping("/signup")
	public String signup(UserCreateForm userCreateForm) {
		return "signup_form";
	}

	@PostMapping("/signup")
	public String signup(@Valid UserCreateForm userCreateForm, BindingResult bindingResult,
			@RequestParam("id") String id) {
		if (bindingResult.hasErrors()) {
			return "signup_form";
		}

		// 제약조건 추가
		if (!userCreateForm.getPassword1().equals(userCreateForm.getPassword2())) {
			bindingResult.rejectValue("password2", "passwordInCorrect", "2개의 패스워드가 일치하지 않습니다.");
			return "signup_form";
		}
		if (userService.checkIdDuplication(id) == true) {
			bindingResult.rejectValue("id", "IdDuplication", "해당 Id는 사용할 수 없습니다.");
			return "signup_form";
		}
		if (userCreateForm.getDOB() == null) {
			bindingResult.rejectValue("DOB", "DOBnotempty", "생년월일은 필수항목입니다.");
			return "signup_form";
		}

		userService.create(userCreateForm.getId(), userCreateForm.getPassword1(), userCreateForm.getName(),
				userCreateForm.getAddress(), userCreateForm.getDOB());

		return "redirect:/";
	}

	@GetMapping("/login")
	public String login() {
		return "login_form";
	}

	@GetMapping("/find_Id")
	public String find_Id() {

		return "find_id";
	}

	@PostMapping("/find_Id")
	public String find_Id(@RequestParam("name") String name, @RequestParam("DOB") String DOB, Model model) {
		if (userService.checkNameDOB(name, DOB) == true) {
			model.addAttribute("result", userService.getId(name));
		} else {
			model.addAttribute("result", "사용자를 찾을수 없습니다.");
		}
		return "find_id_result";
	}

	@GetMapping("/find_Pw")
	public String find_Pw() {

		return "find_pw";
	}

	@PostMapping("/find_Pw")
	public String find_Pw(@RequestParam("id") String id, @RequestParam("name") String name,
			@RequestParam("DOB") String DOB, Model model) {

		String temp_pw;

		if (userService.checkIdNameDOB(id, name, DOB) == true) {
			UUID uid = UUID.randomUUID();
			temp_pw = uid.toString().substring(0, 12);
			userService.changePw(id, temp_pw);
			model.addAttribute("result", temp_pw);
		} else {
			model.addAttribute("result", "사용자를 찾을수 없습니다.");
		}
		return "find_pw_result";
	}

	@GetMapping("/userdetail")
	public String userdetail(Authentication authentication, Model model) {

		model.addAttribute("changeNameForm", new ChangeNameForm());
		model.addAttribute("changeDOBForm", new ChangeDOBForm());

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {
			String id = authentication.getName();
			String name = userService.getName(id);

			SiteUser siteUser = userService.getSiteUser(id);

			model.addAttribute("user", siteUser);

			model.addAttribute("name", name);
		}

		return "userdetail";
	}

	@GetMapping("/change_pw")
	public String change_pw(Authentication authentication, Model model) {
		model.addAttribute("changePWForm", new ChangePWForm());

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {
			String id = authentication.getName();
			String name = userService.getName(id);

			model.addAttribute("name", name);
		}
		return "change_pw";
	}

	@PostMapping("/change_pw")
	public String change_pw(@Valid ChangePWForm ChangePWForm, BindingResult bindingResult,
			Authentication authentication, @RequestParam("password1") String password, Model model) {

		if (bindingResult.hasErrors()) {
			// 사용자가 로그인 상태인지 확인
			if (authentication != null && authentication.isAuthenticated()) {
				String id = authentication.getName();
				String name = userService.getName(id);

				model.addAttribute("name", name);
			}
			return "change_pw";
		}

		// 제약조건 추가
		if (!ChangePWForm.getPassword1().equals(ChangePWForm.getPassword2())) {
			// 사용자가 로그인 상태인지 확인
			if (authentication != null && authentication.isAuthenticated()) {
				String id = authentication.getName();
				String name = userService.getName(id);

				model.addAttribute("name", name);
			}
			
			bindingResult.rejectValue("password2", "passwordInCorrect", "2개의 패스워드가 일치하지 않습니다.");
			return "change_pw";
		}

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {

			String id = authentication.getName();
			String name = userService.getName(id);

			model.addAttribute("name", name);

			// 제약조건 추가
			if (userService.checkPWDuplication(id, password) == true) {
				bindingResult.rejectValue("password1", "passwordDuplication", "기존의 패스워드은 사용 불가 입니다.");
				return "change_pw";
			}

			userService.changePw(id, password);
		}

		return "redirect:/user/userdetail";
	}

	@PostMapping("/change_name")
	public String change_name(@Valid ChangeNameForm ChangeNameForm, BindingResult bindingResult,
			Authentication authentication, @RequestParam("name") String U_name, Model model) {

		if (bindingResult.hasErrors()) {
			model.addAttribute("changeNameForm", ChangeNameForm);
			model.addAttribute("changeDOBForm", new ChangeDOBForm());

			// 사용자가 로그인 상태인지 확인
			if (authentication != null && authentication.isAuthenticated()) {
				String id = authentication.getName();
				String name = userService.getName(id);

				SiteUser siteUser = userService.getSiteUser(id);

				model.addAttribute("user", siteUser);

				model.addAttribute("name", name);
			}
			return "userdetail";
		}

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {

			String id = authentication.getName();
			String name = userService.getName(id);

			model.addAttribute("name", name);
			userService.changeName(id, U_name);
		}

		return "redirect:/user/userdetail";
	}

	@PostMapping("/change_DOB")
	public String change_DOB(@Valid ChangeDOBForm ChangeDOBForm, BindingResult bindingResult,
			Authentication authentication, @RequestParam("DOB") String DOB, Model model) {

		if (bindingResult.hasErrors()) {
			model.addAttribute("changeNameForm",new ChangeNameForm());
			model.addAttribute("changeDOBForm", ChangeDOBForm);

			// 사용자가 로그인 상태인지 확인
			if (authentication != null && authentication.isAuthenticated()) {
				String id = authentication.getName();
				String name = userService.getName(id);

				SiteUser siteUser = userService.getSiteUser(id);

				model.addAttribute("user", siteUser);

				model.addAttribute("name", name);
			}
			return "userdetail";
		}

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {

			String id = authentication.getName();
			String name = userService.getName(id);

			model.addAttribute("name", name);
			userService.changeDOB(id, DOB);
		}

		return "redirect:/user/userdetail";
	}
}
