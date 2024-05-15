package com.example.demo.from;

import jakarta.validation.constraints.*;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ChangeNameForm {
	@NotEmpty(message = "이름은 필수항목입니다.")
    private String name;
}
