from pathlib import Path

ASSETS = Path("assets")

# ==========================================
# LOGO / LOGO_ICON — prefer transparent icon PNG
# ==========================================

_ICON_PNG = ASSETS / "logo_icon.png"
_LOGO_PNG = ASSETS / "logo.png"
_LOGO_JPG = ASSETS / "logo.jpg"

if _ICON_PNG.exists():
    LOGO = _ICON_PNG
    LOGO_ICON = _ICON_PNG
elif _LOGO_PNG.exists():
    LOGO = _LOGO_PNG
    LOGO_ICON = _LOGO_PNG
elif _LOGO_JPG.exists():
    LOGO = _LOGO_JPG
    LOGO_ICON = _LOGO_JPG
else:
    LOGO = _ICON_PNG
    LOGO_ICON = _ICON_PNG

# ==========================================
# FAVICON — falls back to LOGO if missing
# ==========================================

_FAVICON_PNG = ASSETS / "favicon.png"

FAVICON = _FAVICON_PNG if _FAVICON_PNG.exists() else LOGO

# ==========================================
# APP INFO
# ==========================================

APP_NAME = "HealthVibe AI"

APP_SLOGAN = "Vibe Better, Live Better"