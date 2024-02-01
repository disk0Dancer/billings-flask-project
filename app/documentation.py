from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

from app import app

class CreateInputSchema(Schema):
    amount = fields.Int(description="Сумма", required=True, example=500)
    requisite_id = fields.Int(description="Id Реквизитов", required=True, example=1)


class CreateOutputSchema(Schema):
    id = fields.Int(description="Id заявки", required=True, example=1)


class GetInputSchema(Schema):
    id = fields.Int(description="Id заявки", required=True, example=1)


class GetOutputSchema(Schema):
   status = fields.Str(description="Статус заявки", required=True, example="ожидает оплаты")


class ErrorSchema(Schema):
   error = fields.Str(description="Ошибка", example="Ошибка")


def load_docstrings(spec, app):
    """ Загружаем описание API.

    :param spec: объект APISpec, куда загружаем описание функций
    :param app: экземпляр Flask приложения, откуда берем описание функций
    """
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        print(f'Загружаем описание для функции: {fn_name}')
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


def get_apispec(app):
    """ Формируем объект APISpec.

    :param app: объект Flask приложения
    """
    spec = APISpec(
        title="My App",
        version="1.0.0",
        openapi_version="3.0.3",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    spec.components.schema("GetInput", schema=GetInputSchema)
    spec.components.schema("GetOutput", schema=GetOutputSchema)

    spec.components.schema("CreateInput", schema=CreateInputSchema)
    spec.components.schema("CreateOutput", schema=CreateOutputSchema)
    spec.components.schema("Error", schema=ErrorSchema)

    load_docstrings(spec, app)

    return spec