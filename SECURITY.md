# Security Policy

## Supported Versions

We take security seriously. The following versions of Agente CV Inteligente are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We appreciate your efforts to responsibly disclose security vulnerabilities. If you discover a security issue, please follow these guidelines:

### 🔒 How to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by:

1. **Email**: Send details to `security@ejemplo.com`
2. **Subject**: Include `[SECURITY]` in the subject line
3. **Details**: Include as much information as possible:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### 📋 What to Include

Please include the following information in your report:

- **Vulnerability Description**: Clear description of the issue
- **Affected Components**: Which parts of the system are affected
- **Attack Scenario**: How the vulnerability could be exploited
- **Impact Assessment**: Potential consequences
- **Proof of Concept**: Code or steps to reproduce (if applicable)
- **Environment Details**: OS, Python version, dependencies versions

### ⏱️ Response Timeline

We will acknowledge receipt of your vulnerability report within **48 hours** and will send a more detailed response within **7 days** indicating the next steps in handling your report.

We will keep you informed of the progress throughout the process and may ask for additional information or guidance.

### 🛡️ Security Best Practices

When using Agente CV Inteligente:

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use `.env` files that are gitignored
3. **Network Security**: Use HTTPS in production
4. **Input Validation**: Validate all user inputs
5. **Dependencies**: Keep dependencies updated
6. **Access Control**: Implement proper authentication if needed

### 🔍 Known Security Considerations

- **OpenAI API Keys**: Ensure your OpenAI API keys are kept secure
- **SQL Injection**: FAQ SQL tool uses parameterized queries
- **CORS**: Configure CORS properly in production
- **Rate Limiting**: Implement rate limiting for public APIs

### 📊 Security Testing

We regularly perform:

- Dependency vulnerability scanning
- Static code analysis
- Input validation testing
- API security testing

### 🏆 Recognition

We believe in giving credit where credit is due. If you report a valid security issue, we will:

- Credit you in our security advisories (unless you prefer to remain anonymous)
- Include you in our Hall of Fame
- Provide a detailed timeline of the fix

### 📞 Contact Information

For any security-related questions or concerns:

- **Security Email**: security@ejemplo.com
- **Response Time**: Within 48 hours
- **Encryption**: PGP key available upon request

Thank you for helping keep Agente CV Inteligente secure! 🛡️