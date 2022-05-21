"""Application main."""
from project.load import load_iris_data

if __name__ == "__main__":
    iris_data = load_iris_data()
    print(iris_data)
