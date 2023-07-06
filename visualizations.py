from catalog import Catalog


def main():
  catalog = Catalog.load()
  catalog.generate()

if __name__ == '__main__':
  main()
