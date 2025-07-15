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
    <div style="margin: 0.75rem 0 1.5rem 0;">
        <div style="display: flex; align-items: center;">
            <!-- Using CSS to crop the logo to show only the app name, hiding the "Ever Booming" text -->
            <div style="flex: 0 0 auto; overflow: hidden; height: 70px; width: 150px; position: relative;">
                <img src="data:image/png;base64,{LOGO_BASE64}" 
                     alt="MetriBurn Logo"
                     style="position: absolute; height: 85px; width: 300px; object-fit: cover; object-position: 0% 30%; top: -10px; left: 0;">
            </div>
            
            <!-- Description stacked beside the logo -->
            <div style="flex: 1; margin-left: 0.75rem;">
                <p style="margin: 0; padding: 0; font-size: 1.1rem; color: #E0E0E0; line-height: 1.3;">Smart Calorie Tracking for Your Active Lifestyle</p>
                <p style="margin: 0; padding: 0; font-size: 0.85rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.5px; line-height: 1.3;">Powered by Ever Booming Health and Wellness®</p>
            </div>
        </div>
    </div>
    """
