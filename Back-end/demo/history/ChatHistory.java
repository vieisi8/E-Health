package com.example.demo.history;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;
import jakarta.persistence.ManyToOne;

import java.time.LocalDateTime;
import java.util.List;

import com.example.demo.user.SiteUser;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
public class ChatHistory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long number;
    
    private String code;
    
    private String question;
    
    @Lob
    private String answer;
    
    private List <String> image_urls;
    
    private List <String> video_urls;

    private LocalDateTime timestamp;
    
    @ManyToOne
    private SiteUser user;
}
