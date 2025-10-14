from repository import load_repository_data

def get_package_dependencies(package_name: str, version: str, repo_path: str, mode: str):
    """
    Возвращает список прямых зависимостей пакета.
    """
    repo_data = load_repository_data(repo_path, mode)

    if package_name not in repo_data:
        raise ValueError(f"Пакет {package_name} не найден в репозитории.")

    versions = repo_data[package_name]
    # Ищем точную версию или версию, которая начинается с указанной
    matched_version = None
    for ver in versions:
        if ver.startswith(version):
            matched_version = ver
            break

    if not matched_version:
        raise ValueError(f"Версия {version} не найдена для пакета {package_name}.")

    return versions[matched_version]








