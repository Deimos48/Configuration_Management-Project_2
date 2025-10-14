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
    """Возвращает граф зависимостей (DFS)."""
    repo_data = load_repository_data(repo_path, mode)
    graph = {}

    def dfs(pkg, depth, visited):
        if depth > max_depth:
            return
        if pkg in visited:
            graph.setdefault(pkg, []).append("(цикл)")
            return
        visited.add(pkg)
        deps = repo_data.get(pkg, {}).get(version, [])
        graph[pkg] = deps.copy()
        for dep in deps:
            dfs(dep, depth + 1, visited.copy())

    dfs(package_name, 1, set())
    return graph


def get_reverse_dependency_graph(package_name: str, version: str, repo_path: str, mode: str, max_depth: int = 10):
    """Возвращает граф обратных зависимостей — какие пакеты зависят от данного."""
    repo_data = load_repository_data(repo_path, mode)
    reverse_graph = {}

    # Построим обратные связи: кто зависит от кого
    for pkg, versions in repo_data.items():
        for ver, deps in versions.items():
            for dep in deps:
                reverse_graph.setdefault(dep, []).append(pkg)

    graph = {}

    def dfs(pkg, depth, visited):
        if depth > max_depth:
            return
        if pkg in visited:
            graph.setdefault(pkg, []).append("(цикл)")
            return
        visited.add(pkg)
        deps = reverse_graph.get(pkg, [])
        graph[pkg] = deps.copy()
        for dep in deps:
            dfs(dep, depth + 1, visited.copy())

    dfs(package_name, 1, set())
    return graph
