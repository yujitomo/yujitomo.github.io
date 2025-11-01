from os import listdir
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from jinja2 import Template


class MyAssetData(BaseModel):
    href: str
    view_name: str
    asset_type: Literal["article", "solution", "note"]


MY_ASSETS: list[MyAssetData] = [
    MyAssetData(href="https://doi.org/10.2996/kmj47304", view_name="Master", asset_type="article"),
    MyAssetData(href="https://www.ms.u-tokyo.ac.jp/journal/abstract/jms310204.html", view_name="Doctor", asset_type="article"),
]


def read_assets() -> list[MyAssetData]:
    pdfs = [os.path.splitext(f)[0] for f in listdir(Path(__file__).parent / "assets") if os.path.splitext(f)[1] == ".pdf"]
    return [MyAssetData(href=f"https://yujitomo.github.io/assets/{filename}.pdf", view_name=filename, asset_type="note") for filename in pdfs]


def create_page() -> None:

    articles = []
    solutions = []
    notes = []
    for asset in MY_ASSETS:
        if asset.asset_type == "article":
            articles.append(asset)
        if asset.asset_type == "solution":
            solutions.append(asset)
        if asset.asset_type == "note":
            notes.append(asset)

    contents = {"page_title": "ゆじ 倉庫", "my_assets": MY_ASSETS + read_assets(), "articles": articles, "solutions": solutions, "notes": notes}

    with (Path(__file__).parent / "template.html").open("r", encoding="utf-8") as f:
        template = Template(f.read())
    with (Path(__file__).parent / "index.html").open("w", encoding="utf-8") as f:
        f.write(template.render(contents))


if __name__ == "__main__":
    create_page()
