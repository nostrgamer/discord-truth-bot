# Security Policy

## Security Best Practices

### Bot Token Security
- Never share your Discord bot token publicly
- Never commit your `.env` file to version control
- Rotate your bot token if it's ever exposed
- Use environment variables for all sensitive data

### API Token Security
- Keep your Apify API token secure
- Rotate API tokens regularly
- Use the minimum required permissions for API tokens
- Monitor API usage for suspicious activity
- Never share API tokens in code or documentation

### Bot Permissions
- Use the minimum required permissions for your bot
- Regularly review and audit bot permissions
- Remove the bot from servers where it's no longer needed

### Development Security
- Always use a virtual environment
- Keep dependencies up to date
- Review third-party package security
- Use strong, unique passwords for development accounts
- Test API integrations in a development environment first

### Production Security
- Run the bot on a secure server
- Use proper firewall configurations
- Implement rate limiting where appropriate
- Monitor bot activity for suspicious behavior
- Set up API usage alerts and monitoring

## Contributing Security Guidelines

1. Never include sensitive information in pull requests
2. Follow the principle of least privilege
3. Document any security-related changes
4. Test changes in a development environment first
5. Review API integration security implications

## Security Checklist for New Features

- [ ] Input validation implemented
- [ ] Error messages don't expose sensitive information
- [ ] Rate limiting considered
- [ ] Permissions properly scoped
- [ ] Security implications documented
- [ ] API token usage minimized
- [ ] API response caching implemented where appropriate
- [ ] Error handling for API failures
- [ ] Rate limiting for API calls 
