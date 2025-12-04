import sys

try:
    from .connection_module import ConnectToMySQL
except Exception:
    ...

if __name__ == "__main__":
    sys.exit()

__all__ = [ConnectToMySQL]
