import argparse
import sys
from parser_apk import get_package_dependencies

def main():
    parser = argparse.ArgumentParser(description="Этап 2: Сбор данных о зависимостях")
    parser.add_argument("--package", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--mode", choices=["real", "test"], required=True)
    args = parser.parse_args()

    print("Параметры запуска:")
    for arg, val in vars(args).items():
        print(f"{arg}: {val}")

    try:
        deps = get_package_dependencies(args.package, args.version, args.repo, args.mode)
        print(f"\nПрямые зависимости пакета {args.package} ({args.version}):")
        if deps:
            for d in deps:
                print(" -", d)
        else:
            print(" (нет зависимостей)")
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
