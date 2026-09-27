class PublicContexts:
    AUTHENTICATION = "system.auth"
    SOCIAL_LOGIN = "system.auth.social"
    SMS_CALLBACK = "system.sms.callback"

    NAMES = frozenset({AUTHENTICATION, SOCIAL_LOGIN, SMS_CALLBACK})
