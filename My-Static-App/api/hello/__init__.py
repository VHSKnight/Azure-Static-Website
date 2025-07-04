import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Hello function called.')
    return func.HttpResponse("Hello, world!", status_code=200)