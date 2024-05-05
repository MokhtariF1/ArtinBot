from telethon import Button


def paginate(data_prefix, current_page=1, total_pages=1, delimiter=':', before=None, after=None):
    data_prefix += delimiter
    keyboard = []
    if total_pages > current_page + 1:
        keyboard.append(Button.inline('آخر', str.encode(data_prefix + str(total_pages))))
    if total_pages > current_page:
        keyboard.append(Button.inline('بعدی', str.encode(data_prefix + str(current_page + 1))))
    if total_pages > 1:
        keyboard.append(Button.inline(str(current_page) + ' ' + 'از' + ' ' + str(total_pages)))
    if current_page > 1:
        keyboard.append(Button.inline('قبلی', str.encode(data_prefix + str(current_page - 1))))
    if current_page > 2:
        keyboard.append(Button.inline('اول', str.encode(data_prefix + '1')))
    if before or after:
        keyboard = [keyboard]
    if before:
        keyboard = before + keyboard
    if after:
        keyboard.append(after)
    return keyboard
