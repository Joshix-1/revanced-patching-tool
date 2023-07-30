import sys

from .patch import create_patched_apk

sys.exit(create_patched_apk(
    "com.google.android.youtube",
    {
        "Client spoof",
        "Copy video url",
        "Custom branding",
        "Hide Shorts components",
        "External downloads",
        "Hide ads",
        "Hide breaking news shelf",
        "Hide email address",
        "Hide floating microphone button",
        "Hide player buttons",
        "Hide video action buttons",
        "Hide watch in VR",
        "Hide watermark",
        "Minimized playback",
        "Navigation buttons",
        "Old video quality menu",
        "Open links externally",
        # "premium-heading",
        "Remember video quality",
        "Return YouTube Dislike",
        "SponsorBlock",
        "Swipe controls",
        "Theme",
        "Vanced MicroG support",
        "Video ads",
        "Playback speed",
    },
))
