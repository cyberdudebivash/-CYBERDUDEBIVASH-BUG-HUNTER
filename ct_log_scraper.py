import aiohttp


async def fetch_ct_subdomains(domain):

    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    subs = set()

    try:

        async with aiohttp.ClientSession() as session:

            async with session.get(url, timeout=20) as resp:

                if resp.status != 200:
                    return []

                data = await resp.json(content_type=None)

                for entry in data:

                    name = entry.get("name_value")

                    if not name:
                        continue

                    for sub in name.split("\n"):

                        sub = sub.strip()

                        if domain in sub:
                            subs.add(sub)

    except Exception as e:

        print(f"[CT] error: {e}")

    return list(subs)