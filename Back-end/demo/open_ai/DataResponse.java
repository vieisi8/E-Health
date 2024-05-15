package com.example.demo.open_ai;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class DataResponse {
	private String answer;
	private List<String> Image_urls;
    private List<String> Video_urls;
    
	@JsonCreator
	public DataResponse(@JsonProperty("Answer") String answer, @JsonProperty("Image_url") List<String> Image_urls, @JsonProperty("Video_url") List<String> Video_urls) {
		this.answer = answer;
		this.Image_urls=Image_urls;
		this.Video_urls=Video_urls;
	}
}
