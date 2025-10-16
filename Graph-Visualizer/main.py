import argparse
import sys
from parser_apk import get_dependency_graph
from plantuml import PlantUML


def print_graph(graph, root, prefix="", visited=None, is_last=True):
    """ASCII-дерево графа"""
    if visited is None:
        visited = set()
    branch = "└─ " if is_last else "├─ "
    print(prefix + branch + root)
    if root in visited:
        return
    visited.add(root)
    deps = graph.get(root, [])
    n = len(deps)
    for i, dep in enumerate(deps):
        last = (i == n - 1)
        new_prefix = prefix + ("   " if is_last else "│  ")
        if dep == "(цикл)":
            print(new_prefix + ("└─ " if last else "├─ ") + "(цикл)")
        else:
            print_graph(graph, dep, new_prefix, visited.copy(), last)


def graph_to_plantuml(graph, output_file="APK/graph.puml"):
    """Сохраняет граф в формате PlantUML"""
    lines = ["@startuml"]
    for pkg, deps in graph.items():
        for dep in deps:
            if dep != "(цикл)":
                lines.append(f"{pkg} --> {dep}")
    lines.append("@enduml")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"PlantUML файл сохранён: {output_file}")
    return output_file


def render_plantuml_png(puml_file, output_file="APK/graph.png"):
    """Создаёт PNG через PlantUML сервер"""
    server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
    server.processes_file(puml_file)
    print(f"PNG изображение создано: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Этап 5: Визуализация графа зависимостей")
    parser.add_argument("--package", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--mode", choices=["real", "test"], required=True)
    parser.add_argument("--max-depth", type=int, default=10)
    parser.add_argument("--visualize", action="store_true", help="Создать PNG графа зависимостей")
    parser.add_argument("--output", default="graph.png", help="Имя файла PNG")
    args = parser.parse_args()

    print("Параметры запуска:")
    for arg, val in vars(args).items():
        print(f"{arg}: {val}")

    try:
        graph = get_dependency_graph(args.package, args.version, args.repo, args.mode, args.max_depth)
        print(f"\nГраф зависимостей для пакета {args.package} ({args.version}):")
        print_graph(graph, args.package)

        if args.visualize:
            puml_file = graph_to_plantuml(graph)
            render_plantuml_png(puml_file, args.output)

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
