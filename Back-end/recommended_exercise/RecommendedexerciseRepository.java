package com.example.demo.recommended_exercise;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.example.demo.user.SiteUser;

import java.time.LocalDateTime;
import java.util.List;

public interface RecommendedexerciseRepository extends JpaRepository<Recommended_exercise, Long> {
	@Query("SELECT r.type FROM Recommended_exercise r")
    List<String> findAllTypes();

	List<Recommended_exercise> findByTag(String recommendedTag);
}
