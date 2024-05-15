package com.example.demo.recommended_exercise;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@Component
public class DataLoader implements CommandLineRunner {

	private final RecommendedexerciseRepository exerciseRepository;

	public DataLoader(RecommendedexerciseRepository exerciseRepository) {
		this.exerciseRepository = exerciseRepository;
	}

	@Override
	public void run(String... args) throws Exception {
		// WebClient를 사용하여 데이터를 가져오는 부분
		WebClient webClient = WebClient.create("http://127.0.0.1:5000");

		DataResponse recommended_exercise = webClient.get().uri("/read_date").retrieve()
				.bodyToMono(DataResponse.class).block();

		for (int i = 0; i < recommended_exercise.getExercise_types().size(); i++) {
	        Recommended_exercise exercise = new Recommended_exercise();

	        // i번째 types를 하나의 문자열로 결합
	        String typeString = recommended_exercise.getExercise_types().get(i);
	        exercise.setType(typeString);

	        // i번째 names를 하나의 문자열로 결합
	        String nameString = recommended_exercise.getExercise_names().get(i);
	        exercise.setName(nameString);

	        exerciseRepository.save(exercise);
	    }

	}
}
