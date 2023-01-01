import asyncio
import os
import time


async def create_file(i):
    print(f"Creating #{i} file...")
    with open(os.path.join("files", f"file_{i}.txt"), "w"):
        pass
    print(f"Finished creating #{i} file...")


async def delete_file(filename: str):
    print(f"Deleting '{filename}'...")
    os.unlink(os.path.join("files", filename))
    print(f"Deleted '{filename}'")


async def main():
    delete_speed = None

    if not os.path.isdir('files'):
        os.mkdir('files')
    else:
        files = os.listdir('files')
        if files:
            print("Deleting all files in 'files' folder...")
            start_time = time.perf_counter()

            tasks = [delete_file(filename) for filename in files]
            await asyncio.gather(*tasks)

            end_time = time.perf_counter()

            spent_time = end_time - start_time

            print(f"\n\nTime spent on deleting {len(files)} files: {round(spent_time, 2)} seconds")
            delete_speed = round(len(files) / spent_time, 2)
            print(f"Average speed: {delete_speed} files/second\n\n")

    amount = int(input('How many files to create?\n>>> '))
    print()

    start_time = time.perf_counter()

    tasks = [create_file(i) for i in range(1, amount + 1)]
    await asyncio.gather(*tasks)

    end_time = time.perf_counter()

    spent_time = end_time - start_time

    print(f"\n\nTime spent on creating {amount} files: {round(spent_time, 2)} seconds")
    create_speed = round(amount / spent_time, 2)
    print(f"Average speed: {create_speed} files/second")

    print("\n\n")
    if delete_speed:
        ratio = delete_speed / create_speed

        if ratio > 1:
            print(f"Deleting is {round(ratio * 100, 1)}% faster than creating")
        elif ratio < 1:
            print(f"Creating is {round((1 - ratio) * 100, 1)}% faster than deleting")
        else:
            print(f"Creating and deleting is at the same speed.")

        print(f"Creating speed: {create_speed} files/second\nDeleting speed: {delete_speed} files/second")
    else:
        print("Run this again to get a ratio between creating and deleting speed")

if __name__ == "__main__":
    asyncio.run(main())
