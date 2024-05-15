package com.example.demo.admin;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AdminResponse {
    private List<List<String>> Process;
    private List<List<String>> Error;
    
    @JsonCreator
    public AdminResponse(@JsonProperty("Process") List<List<String>> process,
                        @JsonProperty("Error") List<List<String>> error) {
        this.Process = process;
        this.Error = error;
    }
}

