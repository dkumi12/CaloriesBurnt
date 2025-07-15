# Alternative header layout for MetriBurn app
# This provides a simpler header with larger logo and centered text

def get_alternative_header():
    return """
    <div style="text-align: center; margin: 1.5rem 0 2.5rem 0;">
        <div style="margin-bottom: 1rem;">
            <img src="data:image/png;base64,{LOGO_BASE64}" width="150" height="150" alt="MetriBurn Logo">
        </div>
        <h1 style="margin: 0.5rem 0; font-size: 2.8rem; background: linear-gradient(135deg, #E57373 0%, #FF8A80 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">MetriBurn</h1>
        <p style="margin: 0.3rem 0; padding: 0; font-size: 1.4rem; color: #E0E0E0;">Smart Calorie Tracking for Your Active Lifestyle</p>
        <p style="margin: 0.5rem 0; padding: 0; font-size: 1rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.8px;">Powered by Ever Booming Health and Wellness®</p>
    </div>
    """
