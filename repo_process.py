from github import Github
from config import GH_TOKEN
import pathlib
import requests
import zipfile

g = Github(GH_TOKEN)

def clone_repo(repo_url: str):
    
    repo = g.get_repo(repo_url)
    if not repo:
        return "クローンに失敗しました。URLが正しいか確認してください。"
    
    download_url = repo.get_archive_link(archive_format='zipball')

    pathlib.Path("./temp/repo").mkdir(parents=True, exist_ok=True)

    response = requests.get(download_url)
    response.raise_for_status()

    zip_path = pathlib.Path("./temp")

    with open(zip_path / "repo.zip", "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(zip_path / "repo.zip", 'r') as zip_ref:
        zip_ref.extractall(zip_path / "repo")
        

    return f"リポジトリが正常にクローンされました"


if __name__ == "__main__":
    clone_repo("makaseloli/zatugaku")

