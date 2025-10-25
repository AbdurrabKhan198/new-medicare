# Analytics System Documentation

## Overview
The Mediwell Care website now includes a comprehensive analytics system that tracks visitor behavior, traffic sources, and engagement metrics. This system provides both custom analytics and Google Analytics integration.

## Features

### 1. Visitor Tracking
- **Unique Visitor Identification**: Each visitor gets a unique UUID
- **Session Management**: Track visitor sessions and their duration
- **Device Information**: Browser, operating system, device type
- **Geolocation**: Country and city tracking (with IP geolocation)
- **Bot Detection**: Automatically filters out bot traffic

### 2. Page View Tracking
- **Automatic Page Views**: Every page visit is automatically tracked
- **Time on Page**: Track how long visitors spend on each page
- **Exit Pages**: Identify which pages visitors leave from
- **Bounce Rate**: Calculate single-page visit rates
- **Referrer Tracking**: Track where visitors came from

### 3. Traffic Source Analysis
- **Direct Traffic**: Visitors who type the URL directly
- **Search Engines**: Google, Bing, Yahoo, DuckDuckGo
- **Social Media**: Facebook, Instagram, Twitter, LinkedIn, YouTube, WhatsApp
- **Referral Sites**: Other websites linking to your site
- **UTM Parameters**: Track campaign performance
- **Email Campaigns**: Track email marketing effectiveness

### 4. Event Tracking
- **Form Submissions**: Track contact forms, newsletter signups
- **Button Clicks**: Track important button interactions
- **File Downloads**: Track PDF downloads, documents
- **Video Interactions**: Play, pause, complete video events
- **Scroll Depth**: Track how far visitors scroll
- **Outbound Links**: Track clicks to external websites

### 5. Real-time Analytics
- **Live Visitor Count**: See active visitors in real-time
- **Current Page Views**: Track page views happening now
- **Real-time Traffic Sources**: See current traffic sources
- **Live Visitor Details**: View detailed visitor information

## Analytics Dashboard

### Main Dashboard (`/analytics/`)
- **Key Metrics**: Total visitors, unique visitors, page views, bounce rate
- **Real-time Stats**: Active visitors, average session duration
- **Charts**: Hourly traffic distribution, device breakdown
- **Data Tables**: Top pages, traffic sources, countries, browsers
- **Recent Visitors**: Latest visitor activity

### Real-time Analytics (`/analytics/real-time/`)
- **Active Visitors**: Visitors active in the last 5 minutes
- **Current Page Views**: Page views happening now
- **Real-time Traffic Sources**: Current traffic sources
- **Live Visitor Details**: Detailed visitor information

### Visitor Details (`/analytics/visitor/<visitor_id>/`)
- **Visitor Information**: IP, location, device, browser details
- **Page View Timeline**: Complete visitor journey
- **Events**: All tracked events for the visitor
- **Sessions**: Session history and duration
- **Traffic Sources**: How the visitor found the site

## Data Collection

### Automatic Tracking
The system automatically tracks:
- Page views and navigation
- Time spent on pages
- Device and browser information
- Geographic location
- Traffic sources and referrers
- Form submissions
- Button clicks
- File downloads
- Outbound link clicks
- Scroll depth
- Video interactions

### JavaScript API
You can manually track events using the JavaScript API:

```javascript
// Track custom events
Analytics.track('event_name', 'event_value');

// Track form submissions
Analytics.trackForm(formElement);

// Track clicks
Analytics.trackClick(element);

// Track scroll depth
Analytics.trackScroll();

// Track outbound links
Analytics.trackOutbound(linkElement);

// Track downloads
Analytics.trackDownload(linkElement);
```

## Google Analytics Integration

### Setup
1. Add your Google Analytics ID in the admin panel
2. The system will automatically include Google Analytics tracking
3. Enhanced ecommerce tracking is available
4. Custom event tracking is integrated

### Features
- **Page View Tracking**: Automatic page view tracking
- **Event Tracking**: Custom event tracking
- **Form Tracking**: Form submission tracking
- **Ecommerce Tracking**: Conversion and purchase tracking
- **Custom Dimensions**: Track custom visitor attributes

## Data Export

### Available Formats
- **JSON**: API endpoint for data export
- **CSV**: Download data in CSV format
- **Real-time API**: Get live analytics data

### Export Endpoints
- `/analytics/export/?format=json&type=visitors`
- `/analytics/export/?format=json&type=page_views`
- `/analytics/export/?format=json&type=traffic_sources`

## Privacy and Compliance

### Data Protection
- **IP Anonymization**: Option to anonymize IP addresses
- **Cookie Consent**: Respects cookie consent preferences
- **Data Retention**: Configurable data retention period
- **GDPR Compliance**: Built-in privacy controls

### Settings
- **Track User Behavior**: Enable/disable behavior tracking
- **Anonymize IP**: Hide visitor IP addresses
- **Cookie Consent**: Require consent before tracking
- **Data Retention**: Set how long to keep data

## Admin Interface

### Analytics Settings
- Configure Google Analytics ID
- Set up Google Tag Manager
- Configure Facebook Pixel
- Adjust tracking preferences
- Set data retention policies

### Data Management
- View all visitors and their details
- Monitor page views and events
- Track traffic sources
- Manage sessions
- Export data

## API Endpoints

### Analytics API (`/analytics/api/`)
- **Overview**: Get basic analytics metrics
- **Traffic Sources**: Get traffic source breakdown
- **Hourly Data**: Get hourly traffic distribution
- **Real-time**: Get real-time visitor count

### Tracking API (`/analytics/track/`)
- **Event Tracking**: Track custom events
- **Page Views**: Track page visits
- **Form Submissions**: Track form interactions
- **Clicks**: Track button and link clicks

## Performance Impact

### Optimization
- **Asynchronous Loading**: Analytics scripts load asynchronously
- **Minimal Overhead**: Lightweight tracking code
- **Efficient Queries**: Optimized database queries
- **Caching**: Cached analytics data for better performance

### Monitoring
- **Page Load Time**: Track page performance impact
- **Error Tracking**: Monitor tracking errors
- **Uptime**: Ensure analytics system availability

## Troubleshooting

### Common Issues
1. **No Data Appearing**: Check if analytics middleware is enabled
2. **JavaScript Errors**: Verify analytics.js is loaded correctly
3. **Missing Events**: Check if event tracking is properly implemented
4. **Performance Issues**: Monitor database query performance

### Debug Mode
Enable debug mode to see tracking information in the browser console:
```javascript
// Enable debug mode
window.analyticsDebug = true;
```

## Security

### Data Security
- **Encrypted Storage**: Sensitive data is encrypted
- **Access Control**: Admin-only access to analytics data
- **Rate Limiting**: Prevent abuse of tracking endpoints
- **Input Validation**: Validate all tracking data

### Privacy Controls
- **Opt-out Mechanism**: Allow visitors to opt out
- **Data Deletion**: Ability to delete visitor data
- **Consent Management**: Track consent status
- **Anonymization**: Remove identifying information

## Future Enhancements

### Planned Features
- **Heatmaps**: Visual representation of user interactions
- **A/B Testing**: Built-in A/B testing capabilities
- **Conversion Funnels**: Track user conversion paths
- **Cohort Analysis**: Analyze user behavior over time
- **Predictive Analytics**: AI-powered insights
- **Mobile App Tracking**: Track mobile app usage
- **Offline Tracking**: Track offline interactions

### Integration Options
- **CRM Integration**: Connect with customer management systems
- **Email Marketing**: Integrate with email platforms
- **Social Media**: Track social media engagement
- **E-commerce**: Enhanced e-commerce tracking
- **Customer Support**: Track support interactions

## Support

For technical support or questions about the analytics system:
- Check the admin panel for configuration options
- Review the browser console for JavaScript errors
- Monitor the Django logs for server-side issues
- Contact the development team for advanced features

## Conclusion

The analytics system provides comprehensive tracking and reporting capabilities for the Mediwell Care website. It helps understand visitor behavior, optimize content, and improve user experience while maintaining privacy and compliance standards.
