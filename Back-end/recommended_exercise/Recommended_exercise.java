package com.example.demo.recommended_exercise;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
public class Recommended_exercise {

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long number;
    
	@Lob
    private String type;
	@Lob
    private String name;
	@Lob
    private String tag;
}
