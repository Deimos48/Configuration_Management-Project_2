from repository import load_repository_data


def get_package_dependencies(package_name: str, version: str, repo_path: str, mode: str):
    """Возвращает прямые зависимости пакета."""
    repo_data = load_repository_data(repo_path, mode)
    if package_name not in repo_data:
        raise ValueError(f"Пакет {package_name} не найден в репозитории.")

    versions = repo_data[package_name]
    matched_version = None
    for ver in versions:
        if ver.startswith(version):
            matched_version = ver
            break
    if not matched_version:
        raise ValueError(f"Версия {version} не найдена для пакета {package_name}.")

    return versions[matched_version]


def get_dependency_graph(package_name: str, version: str, repo_path: str, mode: str, max_depth: int = 10):
    """Возвращает граф зависимостей с учётом транзитивности, циклов и глубины."""
    repo_data = load_repository_data(repo_path, mode)
    graph = {}

    def dfs(pkg, depth, visited):
        if depth > max_depth:
            return
        if pkg in visited:
            graph.setdefault(pkg, []).append("(цикл)")
            return
        visited.add(pkg)

        # Найдём ближайшую подходящую версию
        versions = repo_data.get(pkg, {})
        matched_version = None
        for ver in versions:
            if ver.startswith(version):
                matched_version = ver
                break
        if matched_version is None and versions:
            # Если точного совпадения нет — берём первую версию
            matched_version = next(iter(versions))

        deps = versions.get(matched_version, []) if matched_version else []
        graph[pkg] = deps.copy()

        for dep in deps:
            # Удаляем возможные префиксы вроде "so:" из имён зависимостей
            dep_clean = dep.split(":")[-1]
            dfs(dep_clean, depth + 1, visited.copy())

    dfs(package_name, 1, set())
    return graph
