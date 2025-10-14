import os
import tarfile
import urllib.request

def load_repository_data(path_or_url: str, mode: str):
    repo_data = {}

    if mode == "test":
        if not os.path.exists(path_or_url):
            raise FileNotFoundError(f"Файл {path_or_url} не найден.")

        with open(path_or_url, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or ":" not in line:
                    continue
                pkg, deps = line.split(":")
                deps_list = [d.strip() for d in deps.split(",") if d.strip()]
                repo_data[pkg.strip()] = {"1.0": deps_list}
        return repo_data

    elif mode == "real":
        url = path_or_url.rstrip("/") + "/APKINDEX.tar.gz"
        apk_dir = "APK"
        os.makedirs(apk_dir, exist_ok=True)  # создаём папку, если нет
        local_file = os.path.join(apk_dir, "APKINDEX.tar.gz")
        print(f"Скачиваем APKINDEX.tar.gz из {url} в {local_file}...")
        urllib.request.urlretrieve(url, local_file)

        print("Распаковываем APKINDEX...")
        with tarfile.open(local_file, "r:gz") as tar:
            apkindex_file = tar.extractfile("APKINDEX")
            content = apkindex_file.read().decode("utf-8").split("\n\n")

        print("Парсим записи...")
        for entry in content:
            lines = entry.splitlines()
            pkg_name = None
            version = None
            deps = []
            for line in lines:
                line = line.strip()
                if line.startswith("P:"):
                    pkg_name = line[2:].strip()
                elif line.startswith("V:"):
                    version = line[2:].strip()
                elif line.startswith("D:"):
                    deps_line = line[2:].strip()
                    deps = [d for d in deps_line.split() if d]
            if pkg_name and version:
                repo_data.setdefault(pkg_name, {})[version] = deps

        print(f"Загружено {len(repo_data)} пакетов из репозитория.")
        return repo_data

    else:
        raise ValueError(f"Неизвестный режим: {mode}")
