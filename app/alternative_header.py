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
        <div style="display: flex; align-items: center; justify-content: flex-start;">
            <!-- Using a wider width but same height to show more of the logo horizontally -->
            <img src="data:image/png;base64,{LOGO_BASE64}" 
                 width="240" height="80" 
                 alt="MetriBurn Logo"
                 style="object-fit: cover; object-position: 0% 50%; margin-right: 0.5rem;">
        </div>
        <div style="margin-top: 0.4rem; margin-left: 0.5rem;">
            <p style="margin: 0.1rem 0; padding: 0; font-size: 1.1rem; color: #E0E0E0;">Smart Calorie Tracking for Your Active Lifestyle</p>
            <p style="margin: 0.1rem 0; padding: 0; font-size: 0.9rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.5px;">Powered by Ever Booming Health and Wellness®</p>
        </div>
    </div>
    """
