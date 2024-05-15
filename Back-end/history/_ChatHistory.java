package com.example.demo.history;

import java.util.List;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class _ChatHistory {

    private String question;
    private String answer;
    private List<String> Image_urls;
    private List<String> Video_urls;

    
}
