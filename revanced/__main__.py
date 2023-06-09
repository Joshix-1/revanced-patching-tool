import sys

from .patch import create_patched_apk

sys.exit(create_patched_apk(
    "com.google.android.youtube",
    {
        "client-spoof": [],
        "copy-video-url": [],
        "custom-branding": [],
        "disable-shorts-on-startup": [],
        "external-downloads": [],
        "hide-ads": [],
        "hide-breaking-news-shelf": [],
        "hide-email-address": [],
        "hide-floating-microphone-button": [],
        "hide-player-buttons": [],
        "hide-video-action-buttons": [],
        "hide-watch-in-vr": [],
        "hide-watermark": [],
        "minimized-playback": [],
        "navigation-buttons": [],
        "old-quality-layout": [],
        "open-links-externally": [],
        # "premium-heading": [],
        "remember-video-quality": [],
        "return-youtube-dislike": [],
        "sponsorblock": [],
        "swipe-controls": [],
        "theme": [],
        "vanced-microg-support": [],
        "video-ads": [],
        "video-speed": [],
    },
))
