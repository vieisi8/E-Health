package com.example.demo.recommended_exercise;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class DataResponse {
	private List<String> exercise_names;
	private List<String> exercise_types;

	@JsonCreator
	public DataResponse(@JsonProperty("exercise_names") List<String> exercise_names,
			@JsonProperty("exercise_types") List<String> exercise_types) {
		this.exercise_names = exercise_names;
		this.exercise_types = exercise_types;
	}
}
