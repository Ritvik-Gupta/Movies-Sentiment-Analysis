import asyncio


async def factorial(name, number) -> int:
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f


async def somehting() -> tuple[bool, str]:
    return True, "cknvs"


async def main():
    f1, f2, f3, (b, s) = await asyncio.gather(
        factorial("A", 2), factorial("B", 3), factorial("C", 4), somehting()
    )
    print(f1, f2, f3, b, s)


asyncio.run(main())
