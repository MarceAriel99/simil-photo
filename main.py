from ModelComponents.model import Model
from PresenterComponents.presenter import Presenter
from ViewComponents.view import View


def main() -> None:
    model = Model()
    view = View()
    presenter = Presenter(model, view)
    presenter.run()

if __name__ == "__main__":
    main()