from model_components.model import Model
from presenter_components.presenter import Presenter
from view_components.view import View


def main() -> None:
    model = Model()
    view = View()
    presenter = Presenter(model, view)
    presenter.run()

if __name__ == "__main__":
    main()