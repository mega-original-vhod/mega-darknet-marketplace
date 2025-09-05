# asdafolder_report.py
import os
from datetime import datetime

def get_file_ext(filename):
    """Возвращает расширение файла, или 'без расширения'"""
    if '.' not in filename or os.path.splitext(filename)[0] == '':
        return 'без расширения'
    return os.path.splitext(filename)[1].lower()

def format_size(bytes_size):
    """Конвертирует байты в удобный формат: KB, MB, GB"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def main():
    print("📁 Генератор отчёта по папке")
    print("—" * 60)

    folder = input("Путь к папке: ").strip()
    if not os.path.exists(folder):
        print("❌ Папка не найдена.")
        return
    if not os.path.isdir(folder):
        print("❌ Указанный путь — не папка.")
        return

    print("\n🔄 Сканируем файлы...")

    ext_count = {}      # Счётчик по расширениям
    ext_size = {}       # Общий размер по расширениям
    all_files = []      # Для поиска самых больших
    total_files = 0
    total_size = 0

    for root, _, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            if not os.path.isfile(filepath):
                continue

            try:
                size = os.path.getsize(filepath)
                ext = get_file_ext(file)

                # Считаем статистику
                ext_count[ext] = ext_count.get(ext, 0) + 1
                ext_size[ext] = ext_size.get(ext, 0) + size
                total_size += size
                total_files += 1

                # Сохраняем для топа
                all_files.append((filepath, size))

            except Exception as e:
                print(f"⚠️  Пропущен файл {file}: {e}")

    # Сортируем файлы по размеру (топ-5 самых больших)
    top_largest = sorted(all_files, key=lambda x: x[1], reverse=True)[:5]

    # Генерация отчёта
    report = []
    report.append("📋 ОТЧЁТ ПО ПАПКЕ")
    report.append("=" * 60)
    report.append(f"Папка: {folder}")
    report.append(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Всего файлов: {total_files}")
    report.append(f"Общий размер: {format_size(total_size)}")
    report.append("")

    report.append("📂 Файлы по типам:")
    report.append("—" * 60)
    
    # Сортируем расширения по количеству
    for ext in sorted(ext_count, key=ext_count.get, reverse=True):
        count = ext_count[ext]
        size = format_size(ext_size[ext])
        report.append(f"{ext:15} — {count:4} файл(ов), {size}")

    report.append("")
    report.append("🏆 Топ-5 самых больших файлов:")
    report.append("—" * 60)
    for i, (path, size) in enumerate(top_largest, 1):
        short_path = path.replace(folder, "...") if len(path) > 50 else path
        report.append(f"{i}. {format_size(size)} — {short_path}")

    # Вывод в консоль
    print("\n".join(report))

    # Сохранение в файл
    report_file = os.path.join(folder, "folder_report.txt")
    counter = 1
    while os.path.exists(report_file):
        name, ext = os.path.splitext(report_file)
        report_file = f"{name}_{counter}{ext}"
        counter += 1

    try:
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        print(f"\n✅ Отчёт сохранён: {report_file}")
    except Exception as e:
        print(f"\n❌ Не удалось сохранить отчёт: {e}")

    print("✨ Анализ завершён.")

if __name__ == "__main__":
    main()
