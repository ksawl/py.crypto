from view.gui_draw import GuiDraw
from utils.file_crud import FileCRUD
from constant import KEYS_DIR, ENCRYPT_DIR, DECRYPT_DIR

if __name__ == "__main__":
    FileCRUD.is_dir_exist(KEYS_DIR)
    FileCRUD.is_dir_exist(ENCRYPT_DIR)
    FileCRUD.is_dir_exist(DECRYPT_DIR)
    GuiDraw()
