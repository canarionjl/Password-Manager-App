from password_manager_controller import password_manager_controller
from password_manager_model import password_manager_model
from password_manager_view import password_manager_view

controller = password_manager_controller()
model = password_manager_model()
view = password_manager_view()


def inject_dependencies():
    view.inject_controller(controller)
    model.inject_controller(controller)
    controller.inject_view_model(model=model, view=view)


inject_dependencies()
controller.configure()
view.init_view()

