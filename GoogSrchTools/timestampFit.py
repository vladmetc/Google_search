"""Reformat news timestamps >> Y-m-d"""
import time


def form_ts(news_ts) -> str:
    """
    :param news_ts: news timestamp string
    :return: Y-m-d date format string
    """
    try:
        unf_dat = time.strptime(news_ts, "%b %d, %Y")
        f_dat = time.strftime("%Y-%m-%d", unf_dat)
        return f_dat
    except ValueError:
        if 'month ago' or 'months ago' in news_ts:
            ep_mon = time.gmtime()[0] * 12 + time.gmtime()[1] - int(news_ts[:1])
            mo_dat = f"{ep_mon // 12}-{ep_mon % 12}"
            return mo_dat
        if 'week ago' or 'weeks ago' in news_ts:
            ep_sec = int(time.time()) - int(news_ts[:1]) * 3600 * 24 * 7
            w_dat = time.strftime('%Y-%m-%d', time.gmtime(int(ep_sec)))
            return w_dat
        if 'day ago' or 'days ago' in news_ts:
            ep_sec = int(time.time()) - int(news_ts[:1]) * 3600 * 24
            d_dat = time.strftime('%Y-%m-%d', time.gmtime(int(ep_sec)))
            return d_dat
        if 'hour ago' or 'hours ago' in news_ts:
            ep_sec = int(time.time()) - int(news_ts[:1]) * 3600
            h_dat = time.strftime('%Y-%m-%d', time.gmtime(int(ep_sec)))
            return h_dat
        if 'minute ago' or 'minutes ago' in news_ts:
            ep_sec = int(time.time()) - int(news_ts[:1]) * 60
            mi_dat = time.strftime('%Y-%m-%d', time.gmtime(int(ep_sec)))
            return mi_dat

        """
        :param cyr_d: string timestamp in Cyrillic
        :return: Y-m-d date format string
        """

        if 'янв.' in news_ts:
            cyr_d = news_ts.replace("янв.", "Jan")
        if 'фев.' in news_ts:
            cyr_d = news_ts.replace("фев.", "Feb")
        if 'мар.' in news_ts:
            cyr_d = news_ts.replace("мар.", "Mar")
        if 'апр.' in news_ts:
            cyr_d = news_ts.replace("апр.", "Apr")
        if 'май.' in news_ts:
            cyr_d = news_ts.replace("май.", "May")
        if 'июн.' in news_ts:
            cyr_d = news_ts.replace("июн.", "Jun")
        if 'июл.' in news_ts:
            cyr_d = news_ts.replace("июл.", "Jul")
        if 'авг.' in news_ts:
            cyr_d = news_ts.replace("авг.", "Aug")
        if 'сен.' in news_ts:
            cyr_d = news_ts.replace("сен.", "Sep")
        if 'окт.' in news_ts:
            cyr_d = news_ts.replace("окт.", "Oct")
        if 'ноя.' in news_ts:
            cyr_d = news_ts.replace("ноя.", "Nov")
        if 'дек.' in news_ts:
            cyr_d = news_ts.replace("дек.", "Dec")
        if 'г.' in news_ts:
            cyr_d = news_ts.replace('г.', '')
        cyr_d = news_ts.strip()
        try:
            unf_dat = time.strptime(cyr_d, "%d %b %Y")
            f_dat = time.strftime("%Y-%m-%d", unf_dat)
            return f_dat
        except ValueError:
            if 'месяц назад' or 'месяца назад' or 'месяцев назад' in cyr_d:
                ep_mon = time.gmtime()[0] * 12 + time.gmtime()[1] - int(cyr_d[:1])
                mo_dat = f"{ep_mon // 12}-{ep_mon % 12}"
                return mo_dat
            if 'неделю назад' or 'недели назад' or 'неделей назад' in cyr_d:
                ep_sec = int(time.time()) - int(cyr_d[:1]) * 3600 * 24 * 7
                w_dat = time.strftime('%Y-%m-%d', time.gmtime(int(ep_sec)))
                return w_dat
            if 'день назад' or 'дня назад' or 'дней назад' in cyr_d:
                ep_sec = int(time.time()) - int(cyr_d[:1]) * 3600 * 24
                d_dat = time.strftime('%Y-%m-%d', time.gmtime(int(ep_sec)))
                return d_dat
            if 'час назад' or 'часа назад' or 'часов назад' in cyr_d:
                ep_sec = int(time.time()) - int(cyr_d[:1]) * 3600
                h_dat = time.strftime('%Y-%m-%d', time.gmtime(int(ep_sec)))
                return h_dat
            if 'минута назад' or 'минуты назад' or 'минут назад' in cyr_d:
                ep_sec = int(time.time()) - int(cyr_d[:1]) * 60
                mi_dat = time.strftime('%Y-%m-%d', time.gmtime(int(ep_sec)))
                return mi_dat

            print(f"Unrecognized timestamp {news_ts}")
            return news_ts
