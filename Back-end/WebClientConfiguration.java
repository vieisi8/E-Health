package com.example.demo;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.codec.ClientCodecConfigurer;
import org.springframework.http.codec.json.Jackson2JsonDecoder;
import org.springframework.http.codec.json.Jackson2JsonEncoder;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfiguration {

    @Bean
    public WebClient webClient() {
        ExchangeStrategies strategies = ExchangeStrategies.builder()
                .codecs(configurer -> {
                    configurer.defaultCodecs().maxInMemorySize(100 * 1024 * 1024); // 100MB로 버퍼 크기 설정
                    configurer.defaultCodecs().enableLoggingRequestDetails(true);
                    configurer.defaultCodecs().jackson2JsonEncoder(new Jackson2JsonEncoder());
                    configurer.defaultCodecs().jackson2JsonDecoder(new Jackson2JsonDecoder());
                })
                .build();

        return WebClient.builder()
                .exchangeStrategies(strategies)
                .baseUrl("http://127.0.0.1:5000")
                .build();
    }
}

