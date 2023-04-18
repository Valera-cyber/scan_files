import zipfile
import xlrd
from xml.etree.ElementTree import iterparse
from search_bad_word import search_regulyar, seach_word


def scaner_file(path_curent_file, list_bad_word, check_regul):
    '''Сканирование файлов'''

    def serch_text(text_in_document, list_bad_word):
        '''Поиск по тексту'''

        if check_regul:
            if search_regulyar(text_in_document):
                return 'regulyar', path_curent_file
            else:
                if seach_word(text_in_document, list_bad_word):
                    return 'word', path_curent_file
        else:
            if seach_word(text_in_document, list_bad_word):
                return 'word', path_curent_file

    def docx(path_curent_file, list_bad_word):
        try:
            '''Сканирование файлов docx'''
            z = zipfile.ZipFile(path_curent_file)
            text_in_document = [el.text for e, el in iterparse(z.open('word/document.xml')) if
                                el.tag.endswith('}t')]
            text_in_document = ' '.join(text_in_document)
            return serch_text(text_in_document, list_bad_word)

        except Exception as e:
            pass
            # logger.error(path_curent_file + ' - ' + str(e))

    # def doc(path_curent_file, list_bad_word):
    #     '''Сканирование doc файлов'''
    #
    #     if '$' not in path_curent_file:
    #
    #         def save_tmp_docx_file(path_curent_file):
    #             '''Сохраняем в текущей директории с именем tmp xxxxxx.docx'''
    #             try:
    #
    #                 w = win32com.client.Dispatch("Word.Application", pythoncom.CoInitialize())
    #                 doc = w.Documents.Open(path_curent_file)
    #
    #                 # print(os.path.basename(path_curent_file))   #имя файла
    #                 # print(os.path.dirname(path_curent_file))  #директория без файла
    #
    #                 tmp_docx_file = (
    #                         os.path.dirname(path_curent_file) + '\\tmp ' + os.path.basename(path_curent_file) + 'x')
    #
    #                 # print(tmp_docx_file)
    #                 doc.SaveAs(tmp_docx_file, 16)
    #                 doc.Close()
    #                 w.Quit()
    #
    #                 return tmp_docx_file
    #             except Exception as e:
    #                 pass
    #                 # logger.error(path_curent_file + ' - ' + str(e))
    #
    #         tmp_docx_file = save_tmp_docx_file(path_curent_file)
    #         # print(tmp_docx_file)
    #
    #         rezult = scan_docx(tmp_docx_file, list_bad_word)
    #
    #         os.remove(tmp_docx_file)
    #
    #         if rezult[0] == 'regulyar':
    #             return 'regulyar', path_curent_file
    #         elif rezult[0] == 'word':
    #             return 'word', path_curent_file

    def xls(path_curent_file, list_bad_word):
        try:
            wb = xlrd.open_workbook(path_curent_file)
            amount_sheets = wb.nsheets
            data = []
            for i in range(amount_sheets):
                ws = wb.sheet_by_index(i)
                for i in range(ws.nrows):
                    for j in range(ws.ncols):
                        if (ws.cell_value(i, j) != ''):
                            data.append(str(ws.cell_value(i, j)))
            # print(' '.join(data))
            text_in_document = (' '.join(data))
            return serch_text(text_in_document, list_bad_word)
        except Exception as e:
            # logger.error(path_curent_file+' - '+ str(e))
            pass

    def xlsx(path_curent_file, list_bad_word):
        try:
            '''Сканирование файлов xlsx'''
            z = zipfile.ZipFile(path_curent_file)
            text_in_document = [el.text for e, el in iterparse(z.open('xl/sharedStrings.xml')) if el.tag.endswith('}t')]
            text_in_document = ' '.join(text_in_document)

            return serch_text(text_in_document, list_bad_word)
        except Exception as e:
            # logger.error(path_curent_file + ' - ' + str(e))

            pass

    def txt(path_curent_file, list_bad_word):
        '''Сканирование файлов txt'''
        try:
            with open(path_curent_file, 'r', encoding="utf-8") as file:
                text_in_document = file.read()
                # print(text_in_document)
                return serch_text(text_in_document, list_bad_word)
        except Exception as e:
            pass
            # logger.error(path_curent_file + ' - ' + str(e))

    if path_curent_file.endswith('.docx'):
        return docx(path_curent_file, list_bad_word)

    # elif path_curent_file.endswith('.doc'):
    #     doc(path_curent_file, list_bad_word)

    elif path_curent_file.endswith('.txt'):
        return txt(path_curent_file, list_bad_word)

    elif path_curent_file.endswith('.xls'):
        return xls(path_curent_file, list_bad_word)

    elif path_curent_file.endswith('.xlsx'):
        return xlsx(path_curent_file, list_bad_word)
