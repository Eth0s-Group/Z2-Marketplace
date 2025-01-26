class InfoBundle:
    def __init__(self, name: str, id: str, version: str, description: str, icon_url: str, download_url: str, store_link: str, summary: str, store_name: str, author_name: str):
        self.name: str = name
        self.id: str = id
        self.version: str = version
        self.description: str = description
        self.summary: str = summary
        self.icon_url: str = icon_url
        self.download_url: str = download_url
        self.store_link: str = store_link
        self.store_name: str = store_name
        self.author_name: str = author_name
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.id,
            "version": self.version,
            "description": self.description,
            "summary": self.summary,
            "icon_url": self.icon_url,
            "download_url": self.download_url,
            "store_link": self.store_link,
            "icon_url": self.icon_url,
            "store_name": self.store_name,
            "author_name": self.author_name
        }

    def __str__(self) -> str:
        return str(self.to_dict())
