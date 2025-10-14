import argparse
import sys
from parser_apk import get_package_dependencies, get_dependency_graph


def print_graph(graph, root, prefix="", visited=None, is_last=True):
    """
    Вывод графа в виде аккуратного ASCII-дерева.
    graph: словарь {pkg: [deps]}
    root: текущий пакет
    prefix: строка отступов
    visited: множество уже посещённых пакетов для обнаружения циклов
    is_last: True если root — последняя ветвь на этом уровне
    """
    if visited is None:
        visited = set()

    # Символ ветви
    branch = "└─ " if is_last else "├─ "
    print(prefix + branch + root)

    if root in visited:
        # Цикл обнаружен
        return
    visited.add(root)

    deps = graph.get(root, [])
    n = len(deps)
    for i, dep in enumerate(deps):
        last = (i == n - 1)
        # Отступ для потомков: если текущий узел последний — пробел, иначе вертикальная линия
        new_prefix = prefix + ("   " if is_last else "│  ")
        if dep == "(цикл)":
            print(new_prefix + ("└─ " if last else "├─ ") + "(цикл)")
        else:
            print_graph(graph, dep, new_prefix, visited.copy(), last)

def main():
    parser = argparse.ArgumentParser(description="Этап 3: Построение графа зависимостей")
    parser.add_argument("--package", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--mode", choices=["real", "test"], required=True)
    parser.add_argument("--max-depth", type=int, default=10)
    args = parser.parse_args()

    print("Параметры запуска:")
    for arg, val in vars(args).items():
        print(f"{arg}: {val}")

    try:
        graph = get_dependency_graph(args.package, args.version, args.repo, args.mode, args.max_depth)
        print(f"\nГраф зависимостей для пакета {args.package} ({args.version}):")
        print_graph(graph, args.package)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
