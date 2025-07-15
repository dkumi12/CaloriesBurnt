# Alternative header layout for MetriBurn app
# This provides a simpler header with larger logo and centered text

def get_alternative_header():
    return """
    <div style="text-align: center; margin: 1rem 0 1.5rem 0;">
        <div style="margin-bottom: 0.5rem;">
            <!-- CSS to zoom and crop the logo to show the text part -->
            <img src="data:image/png;base64,{LOGO_BASE64}" 
                 width="200" height="120" 
                 alt="MetriBurn Logo"
                 style="object-fit: cover; object-position: 0% 50%;">
        </div>
        <p style="margin: 0.2rem 0; padding: 0; font-size: 1.3rem; color: #E0E0E0;">Smart Calorie Tracking for Your Active Lifestyle</p>
        <p style="margin: 0.2rem 0; padding: 0; font-size: 0.95rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.8px;">Powered by Ever Booming Health and Wellness®</p>
    </div>
    """

def get_compact_header():
    return """
    <div style="margin: 1rem 0 2rem 0; text-align: center;">
        <!-- Logo only - using width and height that emphasizes the app name part of the logo -->
        <div style="margin-bottom: 0.75rem; line-height: 0;">
            <img src="data:image/png;base64,{LOGO_BASE64}" 
                 width="180" height="80" 
                 alt="MetriBurn Logo"
                 style="object-fit: contain;">
        </div>
        
        <!-- App description in bold -->
        <p style="margin: 0; padding: 0; font-size: 1.4rem; font-weight: bold; color: #E0E0E0; line-height: 1.4;">
            Smart Calorie Tracking for Your Active Lifestyle
        </p>
        
        <!-- Powered by text in smaller font -->
        <p style="margin: 0.2rem 0 0 0; padding: 0; font-size: 0.8rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.5px; line-height: 1.2;">
            Powered by Ever Booming Health and Wellness®
        </p>
    </div>
    """
