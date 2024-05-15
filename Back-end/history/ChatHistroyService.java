package com.example.demo.history;

import java.security.SecureRandom;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.demo.user.SiteUser;
import com.example.demo.user.UserRepository;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Service
public class ChatHistroyService {
	
	@Autowired
	private final ChatHistoryRepository chathistoryRepository;
	@Autowired
	private final UserRepository userRepository;
	
	private static final SecureRandom secureRandom = new SecureRandom();

	public void create(String userId, String question, String answer, List <String> image_url, List <String> video_url, String code) {
		SiteUser user = userRepository.findById(userId).orElseThrow(() -> new RuntimeException("User not found"));
		
        ChatHistory chathistory = new ChatHistory();
        chathistory.setUser(user);
        chathistory.setQuestion(question);
        chathistory.setAnswer(answer);
        chathistory.setImage_urls(image_url);
        chathistory.setVideo_urls(video_url);
        chathistory.setTimestamp(LocalDateTime.now());
        chathistory.setCode(code);
        
        chathistoryRepository.save(chathistory);
    }
	
	public List<ChatHistory> get(String userId) {
		SiteUser user = userRepository.findById(userId).orElseThrow(() -> new RuntimeException("User not found"));
        return chathistoryRepository.findByUser(user);
    }
	
	public List<ChatHistory> getCode(String code) {
        return chathistoryRepository.findByCode(code);
    }
	
	public Map<String, Map<String, List<ChatHistory>>> getChatHistoryGroupedByDate(String userId) {
        List<ChatHistory> chatHistory = get(userId);

        Map<String, Map<String, List<ChatHistory>>> groupedChatHistory = new HashMap<>();

        for (ChatHistory chat : chatHistory) {
            String dateLabel = getDateLabel(chat.getTimestamp());
            String code = chat.getCode(); // 코드 필드 가져오기
            
         // 날짜 기반으로 그룹화된 맵 가져오기
            Map<String, List<ChatHistory>> dateGroupMap = groupedChatHistory
                    .computeIfAbsent(dateLabel, k -> new HashMap<>());

            // 코드에 따라 그룹화된 리스트 가져오기
            List<ChatHistory> codeGroupList = dateGroupMap
                    .computeIfAbsent(code, k -> new ArrayList<>());

            // 대화 기록 추가
            codeGroupList.add(chat);
        }

        return groupedChatHistory;
    }
	
	public String getDateLabel(LocalDateTime dateTime) {
	    LocalDate currentDate = LocalDate.now();
	    LocalDate chatDate = dateTime.toLocalDate();
	    long daysDifference = ChronoUnit.DAYS.between(chatDate, currentDate);

	    if (daysDifference == 0) {
	        return "A";
	    } else if (daysDifference == 1) {
	        return "B";
	    } else if (daysDifference == 2) {
	        return "C";
	    } else if (daysDifference == 3) {
	        return "D";
	    } else if (daysDifference >= 4 && daysDifference <= 7) {
	        return "E";
	    } else {
	        return "Z";
	    }
	}
	
	public static String generateCode() {
        byte[] randomBytes = new byte[16];
        secureRandom.nextBytes(randomBytes);
        return Base64.getUrlEncoder().encodeToString(randomBytes);
    }
	
}

