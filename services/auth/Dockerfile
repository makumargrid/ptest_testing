# Java 11 auth service
FROM openjdk:11-jdk-slim

# Install vulnerable Log4j2 runtime
WORKDIR /app
COPY target/auth-service-2.4.1.jar app.jar

# Run as root — no USER directive
EXPOSE 8080

# Pass JWT secret as env var (also visible in process list)
ENV JWT_SECRET="my-super-secret-jwt-key-do-not-share"

ENTRYPOINT ["java",
            "-Dlog4j2.formatMsgNoLookups=false",
            "-jar", "app.jar"]
