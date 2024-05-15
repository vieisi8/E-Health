package com.example.demo.user;

import java.time.LocalDate;
import java.util.Optional;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class UserService {

	private final UserRepository userRepository;
	private final PasswordEncoder passwordEncoder;

	public SiteUser create(String id, String password, String name, String address, LocalDate localDate) {
		SiteUser user = new SiteUser();
		user.setId(id);
		user.setPassword(passwordEncoder.encode(password));
		user.setName(name);
		if (address == "") {
			user.setAddress("-");
		} else {
			user.setAddress(address);
		}
		user.setDOB(localDate.toString());
		this.userRepository.save(user);
		return user;
	}

	public boolean checkIdDuplication(String id) {
		return userRepository.existsById(id);
	}

	public boolean checkNameDOB(String name, String DOB) {
		if ((userRepository.existsByName(name) == true) && (userRepository.existsByDOB(DOB) == true)) {
			return true;
		} else {
			return false;
		}
	}

	public String getId(String name) {
		Optional<SiteUser> _siteUser = this.userRepository.findByName(name);
		if (_siteUser.isEmpty()) {
			return "사용자를 찾을수 없습니다.";
		}
		SiteUser siteUser = _siteUser.get();
		return siteUser.getId();
	}

	public String getName(String id) {
		Optional<SiteUser> _siteUser = this.userRepository.findById(id);
		if (_siteUser.isEmpty()) {
			return "사용자를 찾을수 없습니다.";
		}
		SiteUser siteUser = _siteUser.get();
		return siteUser.getName();
	}

	public boolean checkIdNameDOB(String id, String name, String DOB) {
		if ((userRepository.existsById(id)) && (userRepository.existsByName(name) == true)
				&& (userRepository.existsByDOB(DOB) == true)) {
			return true;
		} else {
			return false;
		}
	}

	public void changePw(String id, String temp_pw) {
		SiteUser siteUser = getSiteUser(id);
		siteUser.setPassword(passwordEncoder.encode(temp_pw));
		this.userRepository.save(siteUser);
	}

	public SiteUser getSiteUser(String id) {
		Optional<SiteUser> siteUser = this.userRepository.findById(id);
		return siteUser.get();
	}
	
	public boolean checkPWDuplication(String id, String pw) {
		BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
		SiteUser siteUser = getSiteUser(id);
		return encoder.matches(pw, siteUser.getPassword());
	}
	
	public void changeName(String id, String name) {
		SiteUser siteUser = getSiteUser(id);
		siteUser.setName(name);
		this.userRepository.save(siteUser);
	}
	
	public void changeDOB(String id, String DOB) {
		SiteUser siteUser = getSiteUser(id);
		siteUser.setDOB(DOB);
		this.userRepository.save(siteUser);
	}
}
