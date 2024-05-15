package com.example.demo.open_ai;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.springframework.ui.Model;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.http.MediaType;

import com.example.demo.history._ChatHistory;
import com.example.demo.history.ChatHistory;
import com.example.demo.history.ChatHistroyService;

import jakarta.servlet.http.HttpSession;
import reactor.core.publisher.Mono;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;

@Service
public class Rest_Api_Service {

	@Autowired
	private ChatHistroyService chathistoryservice;

	// 원격 API 호출을 담당하는 메서드
	DataResponse callRemoteAPI(String question, HttpSession session) {
		WebClient webClient = WebClient.create("http://127.0.0.1:5000");

		// Json 형식으로 변환
		String requestBody = String.format("{\"Question\": \"%s\"}", question);

		try {
			// Json Object 변환
			JSONParser parser = new JSONParser();
			JSONObject jsonObject = (JSONObject) parser.parse(requestBody);

			// webClient를 이용한 rest api 호출
			return webClient.post().uri("/").contentType(MediaType.APPLICATION_JSON)
					.body(BodyInserters.fromValue(jsonObject)).retrieve().bodyToMono(DataResponse.class).block();
		} catch (ParseException e) {
			e.printStackTrace();
			// 예외 처리를 필요에 따라 추가
			return null;
		}
	}

	// 통신 결과를 처리하고 세션, 모델에 정보를 추가하는 메서드
	void processApiResponse(String question, DataResponse dataResponse, HttpSession session, Model model,
			Authentication authentication) {
		// 세션에 히스토리 추가
		List<_ChatHistory> chatHistoryList = getChatHistoryFromSession(session);
		_ChatHistory chatHistory = new _ChatHistory();
		chatHistory.setQuestion(question);
		chatHistory.setAnswer(dataResponse.getAnswer());
		chatHistory.setImage_urls(dataResponse.getImage_urls());
		chatHistory.setVideo_urls(dataResponse.getVideo_urls());
		chatHistoryList.add(chatHistory);
		session.setAttribute("chatHistory", chatHistoryList);
		session.setAttribute("session", "ok");

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {
			// 현재 사용자의 아이디를 가져옴
			String id = authentication.getName();

			// 이전 코드를 세션에서 가져오기
			String previousCode = (String) session.getAttribute("code");

			// 로그인된 사용자의 경우에만 실행
			chathistoryservice.create(id, question, dataResponse.getAnswer(), dataResponse.getImage_urls(),
					dataResponse.getVideo_urls(), previousCode);
		}

		// 모델에 추가
		model.addAttribute("chatHistoryList", chatHistoryList);
	}

	List<_ChatHistory> getChatHistoryFromSession(HttpSession session) {
		// 세션에서 히스토리를 가져오기
		Object chatHistoryObj = session.getAttribute("chatHistory");
		Object session_ = session.getAttribute("session");
		if ((chatHistoryObj == null) || (session_ == "off")) {
			return new ArrayList<>();
		} else {
			return (List<_ChatHistory>) chatHistoryObj;
		}
	}

	public void getSidebarContent(Model model, Authentication authentication) {
		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {
			// 현재 사용자의 아이디를 가져옴
			String id = authentication.getName();
			// 날짜별로 채팅을 그룹화하여 가져옴
			Map<String, Map<String, List<ChatHistory>>> groupedChatHistory = chathistoryservice
					.getChatHistoryGroupedByDate(id);

			List<String> keySet = new ArrayList<>(groupedChatHistory.keySet());

			// 키 값으로 오름차순 정렬
			Collections.sort(keySet);

			// 모델에 그룹화된 채팅 내용 추가
			model.addAttribute("GroupedChatHistory", groupedChatHistory);

		}
	}

	// 통신 결과를 처리하고 해당 채팅 내역에 정보를 추가하는 메서드
	void histroy_processApiResponse(String question, DataResponse dataResponse, HttpSession session,
			Authentication authentication) {

		// 사용자가 로그인 상태인지 확인
		if (authentication != null && authentication.isAuthenticated()) {
			// 현재 사용자의 아이디를 가져옴
			String id = authentication.getName();

			// 이전 코드를 세션에서 가져오기
			String previousCode = (String) session.getAttribute("histroy_code");

			// 로그인된 사용자의 경우에만 실행
			chathistoryservice.create(id, question, dataResponse.getAnswer(), dataResponse.getImage_urls(),
					dataResponse.getVideo_urls(), previousCode);
		}
	}
}
