package com.example.demo.user;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface UserRepository extends JpaRepository<SiteUser, Long> {
	
	boolean existsByName(String name);
	boolean existsByDOB(String DOB);
	boolean existsById(String id);
	Optional<SiteUser> findById(String id);
	Optional<SiteUser> findByName(String name);
}
