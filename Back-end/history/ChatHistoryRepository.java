package com.example.demo.history;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.user.SiteUser;

import java.time.LocalDateTime;
import java.util.List;

public interface ChatHistoryRepository extends JpaRepository<ChatHistory, Long> {
	
	List<ChatHistory> findByUser(SiteUser user);

	List<ChatHistory> findByCode(String code);

	void deleteByTimestamp(LocalDateTime sevenDaysAgo);
	
}
