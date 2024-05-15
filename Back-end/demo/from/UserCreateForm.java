package com.example.demo.from;

import java.time.LocalDate;

import jakarta.validation.constraints.*;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UserCreateForm {
    @Size(min = 3, max = 25)
    @NotEmpty(message = "사용자ID는 필수항목입니다.")
    private String id;
    
    @NotEmpty(message = "비밀번호는 필수항목입니다.")
    private String password1;
    
    @NotEmpty(message = "비밀번호 확인은 필수항목입니다.")
    private String password2;
    
    @NotEmpty(message = "이름은 필수항목입니다.")
    private String name;

    private String address;
    
    // birth of date
    @Past(message="당신은 미래에서 오셨습니까?!?!?! 생년월일을 제대로 작성해주세요.")
    private LocalDate DOB;
}
