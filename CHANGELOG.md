# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-25

### Added

#### Backend
- FastAPI application with full REST API
- PostgreSQL database with SQLAlchemy ORM
- User authentication with JWT tokens
- File upload service for Excel trial balance files
- Excel parser with automatic account classification
- Compliance checker implementing Companies Act 2016 requirements
- Risk analyzer for financial anomaly detection
- AI-powered analysis using OpenAI integration
- Report generator for compliance analysis
- Comprehensive error handling and validation
- Logging system with file and console output
- Docker containerization

#### Frontend
- React 18 with TypeScript
- User authentication pages (login, register)
- File upload interface with drag-and-drop
- Dashboard for SME overview
- Compliance report viewer
- Risk level visualization
- Compliance checklist component
- Responsive design with Tailwind CSS
- State management with Zustand
- API integration with axios
- Protected routes for authenticated users

#### Documentation
- Comprehensive API documentation
- Companies Act 2016 compliance reference
- Setup and installation guide
- Production deployment guide
- Contributing guidelines
- Docker Compose configuration

#### Testing
- Backend unit tests for Excel parser
- Compliance checker tests
- API endpoint tests
- Frontend component tests

### Components Included

- **Database Models**: User, Company, Upload, TrialBalanceEntry, ComplianceReport, ComplianceCheckResult
- **API Endpoints**: 15+ RESTful endpoints
- **Services**: Excel parsing, compliance checking, risk analysis, AI analysis, report generation
- **Frontend Pages**: Login, Dashboard, Upload, Reports
- **Compliance Checks**: 10+ automated compliance validations

### Infrastructure
- Docker & Docker Compose setup
- PostgreSQL database with health checks
- Nginx-ready for production
- Environment-based configuration

## Future Roadmap

### [0.2.0] - Planned
- Multi-company support
- Advanced reporting (PDF export)
- Email notifications
- User dashboard with analytics
- Integration with popular accounting software
- API rate limiting
- Audit logging

### [0.3.0] - Planned
- Mobile app (React Native)
- GraphQL API option
- Real-time collaboration
- Workflow automation
- Custom compliance templates

### [1.0.0] - Planned
- Production-ready deployment
- Enterprise features
- SLA support
- White-label options

## Known Limitations

- Single file upload per transaction
- No direct accounting software integration
- AI analysis requires OpenAI API key
- File size limit: 50MB
- Audit trail not implemented

## Support

- GitHub Issues for bug reports
- Email: support@smecompliance.my
- Documentation: /docs folder

## License

MIT License - See LICENSE file
