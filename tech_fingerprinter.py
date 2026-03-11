import aiohttp

SIGNATURES = {
    "nginx": "nginx",
    "apache": "Apache",
    "cloudflare": "cloudflare",
    "wordpress": "wp-content",
    "django": "django",
}


async def fingerprint_host(url):

    found = []

    try:

        async with aiohttp.ClientSession() as session:

            async with session.get(url, ssl=False) as resp:

                body = await resp.text(errors="ignore")

                combined = body + str(resp.headers)

                for tech, sig in SIGNATURES.items():

                    if sig.lower() in combined.lower():

                        found.append(tech)

    except Exception:
        pass

    return found