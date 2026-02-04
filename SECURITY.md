# Security Policy

## Reporting Security Issues

If you discover a security vulnerability in this project, please report it by creating a private security advisory on GitHub or by contacting the maintainers directly.

**Please do not report security vulnerabilities through public GitHub issues.**

## Security Best Practices

### API Key Management

1. **Never commit API keys or secrets to the repository**
   - All API keys must be stored in environment variables
   - Use a `.env` file for local development (already ignored in `.gitignore`)
   - Copy `.env.example` to `.env` and fill in your actual API keys

2. **Required Environment Variables**
   - `GEMINI_API_KEY` or `GOOGLE_API_KEY` - For Google Gemini API
   - `OPENWEATHER_API_KEY` or `WEATHER_API_KEY` - For OpenWeatherMap API

3. **API Key Sources**
   - Get Gemini API key from: https://ai.google.dev/
   - Get OpenWeatherMap API key from: https://openweathermap.org/api

### Secure Communication

- All API requests use HTTPS to ensure data encryption in transit
- API keys are never logged or exposed in error messages

### Dependencies

- Regularly update dependencies to patch security vulnerabilities
- Use `pip list --outdated` to check for available updates
- Review dependency advisories on GitHub

## Known Security Considerations

1. **API Key Security**
   - This application requires API keys to function
   - Keep your `.env` file secure and never share it
   - Rotate your API keys regularly
   - Use API key restrictions when available (e.g., IP restrictions, domain restrictions)

2. **Rate Limiting**
   - Be aware of API rate limits for both Gemini and OpenWeatherMap
   - Implement appropriate error handling for rate limit responses

3. **Input Validation**
   - User input (city names) is validated by the OpenWeatherMap API
   - No direct code execution from user input

## Security Updates

This document was last updated on 2026-02-04. Security practices may evolve over time.
