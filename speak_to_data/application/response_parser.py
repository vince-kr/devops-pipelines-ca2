class Response:
    def __init__(self, model_response: dict) -> None:
        self.model_response = model_response

    @property
    def _has_answer(self) -> bool:
        return "answer" in self.model_response

    @property
    def _has_error(self) -> bool:
        return "error" in self.model_response

    @property
    def is_loading(self) -> bool:
        return self._has_error and "currently loading" in self.model_response["error"]

    @property
    def table_empty(self) -> bool:
        return self._has_error and "table is empty" in self.model_response["error"]

    @property
    def query_empty(self) -> bool:
        return self._has_error and "query is empty" in self.model_response["error"]

    def __str__(self) -> str:
        if self._has_error:
            if self.table_empty:
                return "No data was found based on the previous query."
            elif self.query_empty:
                return "Something went wrong parsing your query. Please attempt to reword it."
        else:
            return self.model_response["answer"]
