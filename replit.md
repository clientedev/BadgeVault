# Overview

This is a Flask-based web application for tracking and managing student badges/certifications from online learning platforms. The system allows instructors to add student profiles via URL, automatically scrapes badge counts from platforms like Google Cloud Skills Boost and Credly, and displays aggregated metrics and individual student data in a dashboard interface.

The application is built for SENAI "Morvan Figueiredo" school, designed to help instructors Gabriel Eduardo and Johnny Braga monitor student progress in obtaining technical certifications.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture

**Framework:** Flask (Python web framework)
- **Rationale:** Lightweight, flexible framework suitable for small-to-medium web applications with straightforward routing needs
- **Session Management:** Uses environment-based secret key for Flask sessions
- **Proxy Support:** ProxyFix middleware to handle reverse proxy headers correctly

**Database Layer:**
- **ORM:** SQLAlchemy with Flask-SQLAlchemy extension
- **Data Model:** Single `Student` model with fields for name, badge count, profile URL, platform, and creation timestamp
- **Schema Design:** Uses DeclarativeBase pattern for model definition
- **Connection Pooling:** Configured with pool recycling (300s) and pre-ping health checks to prevent stale connections

**Web Scraping Strategy:**
- **Multi-method approach:** Combines multiple scraping techniques for robustness
  1. Primary: requests + BeautifulSoup for static HTML parsing
  2. Fallback: Trafilatura for content extraction when standard parsing fails
  3. Advanced: Selenium WebDriver for JavaScript-heavy pages
- **Platform Support:** Google Cloud Skills Boost and Credly profiles
- **Browser Automation:** Headless Chrome with specific flags for containerized environments

**Route Design:**
- `GET /` - Main dashboard showing all students and metrics
- `POST /add_student` - Form submission to add new student profile
- Flash messages for user feedback on operations

## Frontend Architecture

**Design System:** Material Design 3 principles
- **Typography:** Inter font for UI text, JetBrains Mono for technical content
- **Layout:** Responsive grid system using mobile-first approach
- **Components:** Card-based UI for data presentation

**Visualization:**
- Chart.js integration for data visualization
- Metrics dashboard showing totals, averages, and platform-specific counts

**Template Engine:** Jinja2 (Flask's default)
- Server-side rendering for all pages
- Flash message system for operation feedback

**Styling Approach:**
- Custom CSS with Material Design-inspired components
- Responsive breakpoints at 640px (sm), 1024px (lg)
- Sticky header with shadow effects
- Linear gradient background

## Data Flow

1. User submits profile URL via form
2. Backend validates input and initiates scraping
3. Scraper detects platform and applies appropriate extraction logic
4. Student data persisted to database with unique constraint on profile URL
5. Page redirects to dashboard showing updated metrics
6. Frontend calculates and displays aggregated statistics in real-time

## Error Handling

- Flash messages for user-facing errors (invalid URLs, duplicate entries)
- SQLAlchemy IntegrityError handling for duplicate profile URLs
- HTTP timeout configuration (10s) for scraping requests
- Graceful fallbacks in scraping logic when primary methods fail

# External Dependencies

## Third-Party Services

**Learning Platforms (Scraped):**
- Google Cloud Skills Boost - Student certification profiles
- Credly - Digital badge platform profiles

## Python Libraries

**Web Framework:**
- `flask` - Core web framework
- `flask-sqlalchemy` - Database ORM integration

**Web Scraping:**
- `requests` - HTTP client for fetching web pages
- `beautifulsoup4` - HTML parsing library (with lxml parser)
- `trafilatura` - Web content extraction fallback
- `selenium` - Browser automation for dynamic content
- `webdriver` - Chrome WebDriver for Selenium

**Database:**
- `sqlalchemy` - Database toolkit and ORM
- Database engine determined by `DATABASE_URL` environment variable (likely PostgreSQL based on connection pool settings)

**Utilities:**
- `werkzeug` - WSGI utilities including ProxyFix middleware

## Frontend Libraries

- Google Fonts (Inter, JetBrains Mono, Material Icons)
- Chart.js 4.4.0 - Data visualization library via CDN

## Environment Configuration

**Required Environment Variables:**
- `SESSION_SECRET` - Flask session encryption key
- `DATABASE_URL` - Database connection string (SQLAlchemy format)

## Browser Requirements

- Chrome/Chromium browser installed for Selenium scraping
- ChromeDriver compatible with installed Chrome version