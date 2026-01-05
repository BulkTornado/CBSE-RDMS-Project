import sys

if __name__ == "__main__":
    sys.exit()

try:
    from .connection_module import ConnectToMySQL
except (ImportError, ModuleNotFoundError):
    from connection_module import ConnectToMySQL



__all__ = [ConnectToMySQL]
