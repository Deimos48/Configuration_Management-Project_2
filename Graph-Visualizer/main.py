import argparse
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей (Этап 1)"
    )

    parser.add_argument("--package", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--version", required=True, help="Версия пакета")
    parser.add_argument("--repo", required=True, help="URL-адрес репозитория или путь к тестовому репозиторию")
    parser.add_argument("--mode", choices=["real", "test"], required=True, help="Режим работы: real или test")
    parser.add_argument("--output", default="graph.png", help="Имя выходного файла с изображением графа")
    parser.add_argument("--max-depth", type=int, default=3, help="Максимальная глубина анализа зависимостей")
    parser.add_argument("--ascii", action="store_true", help="Вывод зависимостей в формате ASCII-дерева")

    return parser.parse_args()


def validate_args(args):
    errors = []

    if not args.package.strip():
        errors.append("Имя пакета не может быть пустым.")

    if not args.version.strip():
        errors.append("Версия пакета не может быть пустой.")

    if args.mode == "test":
        if not os.path.exists(args.repo):
            errors.append(f"Файл тестового репозитория не найден: {args.repo}")
    else:
        if not (args.repo.startswith("http://") or args.repo.startswith("https://")):
            errors.append(f"Некорректный URL репозитория: {args.repo}")

    if args.max_depth < 1:
        errors.append("Максимальная глубина анализа должна быть положительным числом.")

    if not args.output.endswith(".png"):
        errors.append("Выходной файл должен иметь расширение .png")

    if errors:
        print("❌ Ошибки в параметрах:")
        for err in errors:
            print("  -", err)
        sys.exit(1)


def main():
    args = parse_args()
    validate_args(args)

    print("\n✅ Параметры конфигурации:")
    print(f"package = {args.package}")
    print(f"version = {args.version}")
    print(f"repo = {args.repo}")
    print(f"mode = {args.mode}")
    print(f"output = {args.output}")
    print(f"max_depth = {args.max_depth}")
    print(f"ascii_mode = {args.ascii}")


if __name__ == "__main__":
    main()
