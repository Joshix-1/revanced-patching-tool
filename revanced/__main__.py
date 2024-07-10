import sys

from .patch import create_patched_apk

#sys.exit(create_patched_apk(
#    "de.dwd.warnapp",
#    {"Promo code unlock"},
#    version="4.2.1"
#))
# Not selected patches: 
(
'Always repeat', 
'Announcements', 
'Change header',
 'Change start page', 
 'Comments', 
 'Copy video URL', 
 'Custom player overlay opacity', 
 'Disable auto captions',
  'Disable player popup panels', 
  'Disable precise seeking gesture', 
  'Disable resuming Shorts on startup', 
  'Disable rolling number animations', 
  'Disable suggested video end screen', 
  'Disable zoom haptics', 'Enable debugging', 'Enable slide to seek', 'Enable tablet layout', 'HDR auto brightness', "Hide 'Load more' button", 
  'Hide album cards', 'Hide autoplay button', 'Hide captions button', 'Hide cast button', 'Hide crowdfunding box', 'Hide endscreen cards', 
  'Hide filter bar', 'Hide info cards', 'Hide layout components', 'Hide seekbar', 'Hide timestamp', 'Player flyout menu', 
  'Remove player controls background', 'Remove tracking query parameter', 'Remove viewer discretion dialog', 'Restore old seekbar thumbnails', 
  'Restore old video quality menu', 'Seekbar tapping', 'Spoof app version', 'Spoof device dimensions', 'Tablet mini player', 'Wide searchbar')
# Missing patches: ( 'Disable Shorts on startup', 'Hide email address', 'Hide watermark',)


sys.exit(create_patched_apk(
    "com.google.android.youtube",
    {
        "Announcements",
        "Alternative thumbnails",
        "Change start page",
        "Copy video URL",
        "Custom branding",
        "Disable fullscreen ambient mode",
        "Disable resuming Shorts on startup",
        "Enable slide to seek",
        "Hide Shorts components",
        "Downloads",
        "Hide ads",
        # "Hide breaking news shelf",
        "Hide cast button",
        "Hide floating microphone button",
        "Hide player buttons",
        "Hide video action buttons",
        "Navigation buttons",
        "Open links externally",
        "Player flyout menu",
        "Remember video quality",
        "Remove background playback restrictions",
        "Remove tracking query parameter",
        "Restore old seekbar thumbnails",
        "Restore old video quality menu",
        "Return YouTube Dislike",
        "SponsorBlock",
        "Spoof client",
        "Spoof app version",
        "Swipe controls",
        "Theme",
        "GmsCore support",
        "Video ads",
        "Playback speed",
        "Bypass URL redirects",
    },
))
