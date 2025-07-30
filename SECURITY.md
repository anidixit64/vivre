# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Vivre seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:

**aniketdixit00.ani@gmail.com**

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the requested information listed below (as much as you can provide) to help us better understand the nature and scope of the possible issue:

- Type of issue (buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the vulnerability
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

This information will help us triage your report more quickly.

## Preferred Languages

We prefer all communications to be in English.

## Policy

Vivre follows the principle of [Responsible Disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure).

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**: Regularly update Vivre and its dependencies
2. **Validate Input**: Always validate EPUB files before processing
3. **Use Virtual Environments**: Isolate Vivre installations
4. **Monitor Logs**: Check for unusual activity in your applications

### For Contributors

1. **Follow Secure Coding Practices**: Use type hints, validate inputs, handle exceptions
2. **Test Security**: Include security-focused tests
3. **Review Dependencies**: Regularly audit dependencies for vulnerabilities
4. **Document Security**: Document security considerations in code

### For Maintainers

1. **Regular Audits**: Conduct regular security audits
2. **Dependency Monitoring**: Monitor dependencies for vulnerabilities
3. **Security Testing**: Include security tests in CI/CD
4. **Timely Updates**: Promptly address security issues

## Security Features

Vivre includes several security features:

- **Input Validation**: All EPUB files are validated before processing
- **Safe XML Parsing**: Uses defusedxml for secure XML processing
- **Type Safety**: Comprehensive type hints prevent type-related vulnerabilities
- **Error Handling**: Secure error handling without information disclosure
- **Dependency Security**: Regular dependency updates and monitoring

## Known Issues

None at this time.

## Security Updates

Security updates will be released as patch versions (e.g., 0.1.1, 0.1.2) and will be clearly marked in the changelog.

## Credits

We would like to thank all security researchers and contributors who help keep Vivre secure by responsibly reporting vulnerabilities.
