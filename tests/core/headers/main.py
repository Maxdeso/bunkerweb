from contextlib import suppress
from os import getenv
from requests import RequestException, get, head
from traceback import format_exc
from time import sleep


try:
    ssl = getenv("GENERATE_SELF_SIGNED_SSL", "no") == "yes"

    ready = False
    retries = 0
    while not ready:
        with suppress(RequestException):
            status_code = get(
                f"http{'s' if ssl else ''}://www.example.com",
                headers={"Host": "www.example.com"},
                verify=False,
            ).status_code

            if status_code >= 500:
                print("❌ An error occurred with the server, exiting ...", flush=True)
                exit(1)

            ready = status_code < 400

        if retries > 10:
            print("❌ The service took too long to be ready, exiting ...", flush=True)
            exit(1)
        elif not ready:
            retries += 1
            print(
                "⚠️ Waiting for the service to be ready, retrying in 5s ...", flush=True
            )
            sleep(5)

    custom_headers = getenv("CUSTOM_HEADER", "")
    remove_headers = getenv(
        "REMOVE_HEADERS", "Server X-Powered-By X-AspNet-Version X-AspNetMvc-Version"
    )
    strict_transport_security = getenv("STRICT_TRANSPORT_SECURITY", "max-age=31536000")
    cookie_flags = getenv("COOKIE_FLAGS", "* HttpOnly SameSite=Lax")
    cookie_flags_1 = getenv("COOKIE_FLAGS_1")
    cookie_auto_secure_flag = getenv("COOKIE_AUTO_SECURE_FLAG", "yes") == "yes"
    content_security_policy = getenv(
        "CONTENT_SECURITY_POLICY",
        "object-src 'none'; form-action 'self'; frame-ancestors 'self';",
    )
    referrer_policy = getenv("REFERRER_POLICY", "strict-origin-when-cross-origin")
    permissions_policy = getenv(
        "PERMISSIONS_POLICY",
        "accelerometer=(), ambient-light-sensor=(), autoplay=(), battery=(), camera=(), cross-origin-isolated=(), display-capture=(), document-domain=(), encrypted-media=(), execution-while-not-rendered=(), execution-while-out-of-viewport=(), fullscreen=(), geolocation=(), gyroscope=(), hid=(), idle-detection=(), magnetometer=(), microphone=(), midi=(), navigation-override=(), payment=(), picture-in-picture=(), publickey-credentials-get=(), screen-wake-lock=(), serial=(), usb=(), web-share=(), xr-spatial-tracking=()",
    )
    feature_policy = getenv(
        "FEATURE_POLICY",
        "accelerometer 'none'; ambient-light-sensor 'none'; autoplay 'none'; battery 'none'; camera 'none'; display-capture 'none'; document-domain 'none'; encrypted-media 'none'; execution-while-not-rendered 'none'; execution-while-out-of-viewport 'none'; fullscreen 'none'; geolocation 'none'; gyroscope 'none'; layout-animation 'none'; legacy-image-formats 'none'; magnetometer 'none'; microphone 'none'; midi 'none'; navigation-override 'none'; payment 'none'; picture-in-picture 'none'; publickey-credentials-get 'none'; speaker-selection 'none'; sync-xhr 'none'; unoptimized-images 'none'; unsized-media 'none'; usb 'none'; screen-wake-lock 'none'; web-share 'none'; xr-spatial-tracking 'none';",
    )
    x_frame_options = getenv("X_FRAME_OPTIONS", "SAMEORIGIN")
    x_content_type_options = getenv("X_CONTENT_TYPE_OPTIONS", "nosniff")
    x_xss_protection = getenv("X_XSS_PROTECTION", "1; mode=block")

    print(
        f"ℹ️ Sending a HEAD request to http{'s' if ssl else ''}://www.example.com ...",
        flush=True,
    )

    response = head(
        f"http{'s' if ssl else ''}://www.example.com",
        headers={"Host": "www.example.com"},
        verify=False,
    )
    response.raise_for_status()

    if custom_headers:
        splitted = custom_headers.split(":")

        if response.headers.get(splitted[0].strip()) != splitted[1].strip():
            print(
                f"❌ Header {splitted[0].strip()} is not set to {splitted[1].strip()}, exiting ...\nheaders: {response.headers}",
                flush=True,
            )
            exit(1)
    elif "Server" not in remove_headers and "Server" not in response.headers:
        print(
            f'❌ Header "Server" is not removed, exiting ...\nheaders: {response.headers}',
            flush=True,
        )
        exit(1)
    elif (
        ssl
        and response.headers.get("Strict-Transport-Security")
        != strict_transport_security
    ):
        print(
            f'❌ Header "Strict-Transport-Security" doesn\'t have the right value. {response.headers.get("Strict-Transport-Security", "missing header")} (header) != {strict_transport_security} (env), exiting ...\nheaders: {response.headers}',
            flush=True,
        )
        exit(1)
    elif not ssl and "Strict-Transport-Security" in response.headers:
        print(
            f'❌ Header "Strict-Transport-Security" is present even though ssl is deactivated, exiting ...\nheaders: {response.headers}',
            flush=True,
        )
        exit(1)
    elif response.headers.get("Content-Security-Policy") != content_security_policy:
        print(
            f'❌ Header "Content-Security-Policy" doesn\'t have the right value. {response.headers.get("Content-Security-Policy", "missing header")} (header) != {content_security_policy} (env), exiting ...\nheaders: {response.headers}',
            flush=True,
        )
        exit(1)
    elif response.headers.get("Referrer-Policy") != referrer_policy:
        print(
            f'❌ Header "Referrer-Policy" doesn\'t have the right value. {response.headers.get("Referrer-Policy", "missing header")} (header) != {referrer_policy} (env), exiting ...\nheaders: {response.headers}',
            flush=True,
        )
        exit(1)
    elif response.headers.get("Permissions-Policy") != permissions_policy:
        print(
            f'❌ Header "Permissions-Policy" doesn\'t have the right value. {response.headers.get("Permissions-Policy", "missing header")} (header) != {permissions_policy} (env), exiting ...\nheaders: {response.headers}',
            flush=True,
        )
        exit(1)
    elif response.headers.get("Feature-Policy") != feature_policy:
        print(
            f'❌ Header "Feature-Policy" doesn\'t have the right value. {response.headers.get("Feature-Policy", "missing header")} (header) != {feature_policy} (env), exiting ...\nheaders: {response.headers}',
            flush=True,
        )
        exit(1)
    elif response.headers.get("X-Frame-Options") != x_frame_options:
        print(
            f'❌ Header "X-Frame-Options" doesn\'t have the right value. {response.headers.get("X-Frame-Options", "missing header")} (header) != {x_frame_options} (env), exiting ...\nheaders: {response.headers}',
            flush=True,
        )
        exit(1)
    elif response.headers.get("X-Content-Type-Options") != x_content_type_options:
        print(
            f'❌ Header "X-Content-Type-Options" doesn\'t have the right value. {response.headers.get("X-Content-Type-Options", "missing header")} (header) != {x_content_type_options} (env), exiting ...\nheaders: {response.headers}',
            flush=True,
        )
        exit(1)
    elif response.headers.get("X-XSS-Protection") != x_xss_protection:
        print(
            f'❌ Header "X-XSS-Protection" doesn\'t have the right value. {response.headers.get("X-XSS-Protection", "missing header")} (header) != {x_xss_protection} (env), exiting ...\nheaders: {response.headers}',
            flush=True,
        )
        exit(1)

    if not response.cookies:
        print("❌ No cookies were set, exiting ...", flush=True)
        exit(1)

    cookie = next(iter(response.cookies))

    # Iterate over the cookies and print their values and flags
    if ssl and cookie_auto_secure_flag and not cookie.secure:
        print(
            f"❌ Cookie {cookie.name} doesn't have the secure flag, exiting ...\ncookie: name = {cookie.name}, secure = {cookie.secure}, HttpOnly = {cookie.has_nonstandard_attr('HttpOnly')}",
        )
        exit(1)
    elif (not ssl or not cookie_auto_secure_flag) and cookie.secure:
        print(
            f"❌ Cookie {cookie.name} has the secure flag even though it's not supposed to, exiting ...\ncookie: name = {cookie.name}, secure = {cookie.secure}, HttpOnly = {cookie.has_nonstandard_attr('HttpOnly')}",
        )
        exit(1)
    elif "HttpOnly" not in cookie_flags and cookie.has_nonstandard_attr("HttpOnly"):
        print(
            f"❌ Cookie {cookie.name} has the HttpOnly flag even though it's not supposed to, exiting ...\ncookie: name = {cookie.name}, secure = {cookie.secure}, HttpOnly = {cookie.has_nonstandard_attr('HttpOnly')}",
        )
        exit(1)
    elif (
        not cookie_flags_1
        and "HttpOnly" in cookie_flags
        and not cookie.has_nonstandard_attr("HttpOnly")
    ):
        print(
            f"❌ Cookie {cookie.name} doesn't have the HttpOnly flag even though it's set in the env, exiting ...\ncookie: name = {cookie.name}, secure = {cookie.secure}, HttpOnly = {cookie.has_nonstandard_attr('HttpOnly')}",
        )
        exit(1)

    print("✅ Headers are working as expected ...", flush=True)
except SystemExit:
    exit(1)
except:
    print(f"❌ Something went wrong, exiting ...\n{format_exc()}", flush=True)
    exit(1)
