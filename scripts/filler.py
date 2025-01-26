import fetcher, json
from infobundle import InfoBundle

with open("../skeleton.json", "rt") as skele:
    tree: dict = json.load(skele)

for app_id in tree["apps"].keys():
    app: dict = tree["apps"][app_id]
    if not "type" in app:
        continue
    if app["type"] == "f-droid":
        app_info: InfoBundle = fetcher.get_fdroid(app_id, ignore_recommended=True, repo="https://f-droid.org/repo" if not "repo" in app else app["repo"])
    if app["type"] == "fenix":
        app_info: InfoBundle = fetcher.get_fenix()
    app["name"] = app_info.name
    app["downloadUrl"] = app_info.download_url
    app["attribution"] = {
        "name": app_info.store_name if app_info.store_name == app_info.author_name else f"{app_info.author_name} on {app_info.store_name}",
        "link": app_info.store_link
    }
    app["icon"] = app_info.icon_url
    if not "description" in app:
        app["description"] = ""
    app["description"] += f"\n-----\nFrom {app_info.store_name}:\n{app_info.summary}"

with open("../market.json", "wt") as output:
    json.dump(tree, output, indent="    ")
