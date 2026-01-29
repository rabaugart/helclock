import asyncio

if __name__ == "__main__":
    from .quart import main
    asyncio.run(main())
    print("Gestoppt")
