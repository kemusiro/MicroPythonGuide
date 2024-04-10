def main():
    raise OSError("dummy exception")

try:
    main()
except KeyboardInterrupt:
    print("\nBye!")
except Exception as e:
    print("unexpected exception occurred")
    print(e)
    