import requests
# import yaml
from infobundle import InfoBundle
cached_index: dict = {}
DISK_CACHE_ENABLED: bool = False
if DISK_CACHE_ENABLED:
    import json,time
dirty_cache: bool = False
if DISK_CACHE_ENABLED:
    try:
        with open("cached_index.json") as file:
            cached_index = json.load(file)
            if cached_index["dumped"] - time.time() > 1 * 60 * 60:
                cached_index = {}
    except:
        print("Couldn't read cache")

def get_fdroid(appid: str, ignore_recommended: bool = False, repo: str = "https://f-droid.org/repo") -> InfoBundle:
    global cached_index
    # metadatayaml: str = requests.get(f"https://gitlab.com/fdroid/fdroiddata/-/raw/master/metadata/{appid}.yml").text
    # metadata: dict = yaml.safe_load(metadatayaml)
    # del metadatayaml
    # versioncode: int | None = None
    # version: str | None = None
    # if (ignore_recommended):
    #     versioncode = int(metadata["Builds"][-1]["versionCode"])
    #     version = metadata["Builds"][-1]["versionName"]
    # else:
    #     versioncode = int(metadata["CurrentVersionCode"])
    #     version = metadata["CurrentVersion"]
    if not repo in cached_index:
        print("Couldn't find repo in cache, downloading...")
        cached_index[repo] = requests.get(f"{repo}/index-v2.json").json()
        print("Downloaded!!")
        dirty_cache = True
        
    index_entry: dict = cached_index[repo]["packages"][appid]
    version_manifest: dict = index_entry["versions"][next(iter(index_entry["versions"]))]["manifest"]
    version: str = version_manifest["versionName"]
    versioncode: int = int(version_manifest["versionCode"])
    if not "authorName" in index_entry["metadata"]:
        index_entry["metadata"]["authorName"] = "Anonymous"
    return InfoBundle(
        name=index_entry["metadata"]["name"]["en-US"],
        id=appid,
        version=version,
        description=index_entry["metadata"]["description"]["en-US"],
        download_url=f"{repo}/{appid}_{versioncode}.apk",
        store_link=f"{cached_index[repo]["repo"]["webBaseUrl"]}/{appid}/",
        icon_url=f"{repo}{index_entry["metadata"]["icon"]["en-US"]["name"]}",
        summary=index_entry["metadata"]["summary"]["en-US"],
        store_name=cached_index[repo]["repo"]["name"]["en-US"],
        author_name=index_entry["metadata"]["authorName"]
    )

def get_fenix() -> InfoBundle:
    version = requests.get("https://product-details.mozilla.org/1.0/mobile_versions.json").json()["version"]
    return InfoBundle(
        name="Firefox",
        id="org.mozilla.firefox",
        version=version,
        description="The Firefox web browser for Android.",
        download_url=f"https://ftp.mozilla.org/pub/fenix/releases/{version}/android/fenix-{version}-android-armeabi-v7a/fenix-{version}.multi.android-armeabi-v7a.apk",
        store_link="https://www.mozilla.org/en-US/firefox/browsers/mobile/android/",
        # icon_url="https://hg.mozilla.org/mozilla-central/raw-file/tip/browser/branding/official/default256.png",
        icon_url="https://www.mozilla.org/media/protocol/img/logos/firefox/browser/logo.eb1324e44442.svg",
        summary="Only non-profit-backed browser that is secure, private & fast",
        store_name="Mozilla",
        author_name="Mozilla"
    )

def get_aurora() -> InfoBundle:
    return get_fdroid("com.aurora.store", True)

def get_shizuku() -> InfoBundle:
    return get_fdroid("moe.shizuku.privileged.api", True, "https://apt.izzysoft.de/fdroid/repo")

def get_newpipe() -> InfoBundle:
    return get_fdroid("org.schabi.newpipe", True)

if __name__ == "__main__":
    print(get_aurora())
    print(get_shizuku())
    print(get_newpipe())
    print(get_fenix())
    if DISK_CACHE_ENABLED and dirty_cache:
        cached_index["dumped"] = time.time()
        with open("cached_index.json", "wt") as file:
            json.dump(cached_index, file, indent="\t")