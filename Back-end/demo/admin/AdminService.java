package com.example.demo.admin;

import java.util.List;

import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.ui.Model;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.http.MediaType;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URISyntaxException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;

@Service
public class AdminService {

	private final WebClient webClient;

	public AdminService(WebClient webClient) {
		this.webClient = webClient;
	}

	void get_process(Model model, Authentication authentication) {

		AdminResponse response = webClient.get().uri("/admin/process").retrieve().bodyToMono(AdminResponse.class)
				.block();

		List<List<String>> processList = response.getProcess();

		model.addAttribute("process", processList);

	}

	void get_error_and_prompt(Model model, Authentication authentication) {

		AdminResponse response = webClient.get().uri("/admin/error").retrieve().bodyToMono(AdminResponse.class)
				.block();

		List<List<String>> errorList = response.getError();

		model.addAttribute("error", errorList);

	}

}
