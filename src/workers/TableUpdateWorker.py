from PyQt6.QtCore import QThread, pyqtSignal
import pandas as pd

class TableUpdateWorker(QThread):
    block_ready = pyqtSignal(int, list)
    finished = pyqtSignal(bool, list)
    progress = pyqtSignal(int)
    debug = pyqtSignal(str)

    def __init__(self, dataframe, block_size=900):
        super().__init__()
        self.dataframe = dataframe
        self.block_size = block_size

    def run(self):
        if self.dataframe is None or not isinstance(self.dataframe, pd.DataFrame):
            self.debug.emit("DataFrame é None ou inválido")
            self.finished.emit(False, [])
            return
        if self.dataframe.empty:
            self.debug.emit("DataFrame está vazio")
            self.finished.emit(True, self.dataframe.columns.tolist())
            return

        try:
            headers = self.dataframe.columns.tolist()
            total_rows = len(self.dataframe)
            self.debug.emit(f"Total de linhas: {total_rows}, Colunas: {headers}")

            for start_idx in range(0, total_rows, self.block_size):
                end_idx = min(start_idx + self.block_size, total_rows)
                block_data = [
                    [str(value) for value in row]
                    for row in self.dataframe.iloc[start_idx:end_idx].itertuples(index=False)
                ]
                self.debug.emit(f"Enviando bloco de {start_idx} a {end_idx} com {len(block_data)} linhas")
                self.block_ready.emit(start_idx, block_data)
                self.progress.emit(int((end_idx / total_rows) * 100))

            self.finished.emit(True, headers)
        except Exception as e:
            self.debug.emit(f"Erro no worker: {e}")
            self.finished.emit(False, [f"Error processing table data: {e}"])