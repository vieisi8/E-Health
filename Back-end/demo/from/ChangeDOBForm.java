package com.example.demo.from;

import java.time.LocalDate;

import jakarta.validation.constraints.*;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ChangeDOBForm {
	// birth of date
    @Past(message="당신은 미래에서 오셨습니까?!?!?! 생년월일을 제대로 작성해주세요.")
    private LocalDate DOB;
}
