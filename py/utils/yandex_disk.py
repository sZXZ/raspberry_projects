import requests
import pandas as pd
import numpy as np
from IPython.display import IFrame, HTML, display, Image
from subprocess import run
import yadisk
import cv2
import matplotlib.pyplot as plt
from py.utils import analize_tf_lite as tf_classifier
from py.utils import code_secrets

class YandexDisk(yadisk.YaDisk):
    """
    Instance of yadisk.YaDisk class.
    Custom fuctions:
        a_* used for REST
        r_* for rclone
        h_* for html
    """

    def __init__(self):
        super().__init__(token=code_secrets.TOKEN)
        self.link = "https://disk.yandex.ru/client/disk/"

    def h_link(self, names: pd.Series) -> pd.Series:
        return self.link + names

    def h_get_link(self, row):
        path = "/".join(row.split("/")[:-1])
        path_to_file = "%2F".join(row.split("/"))
        return f"{self.lnik}{path}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{path_to_file}"

    def h_photo_link(self, names: pd.Series) -> pd.Series:
        # Photos/Years/2016/04/recup_dir.146/rec_2016_04_20_143019-00.CR2
        # https://disk.yandex.ru/client/disk/Photos/Years/2016/04/recup_dir.146Photos%2FYears%2F2016%2F04%2Frecup_dir.146%2Frec_2016_04_20_143019-00.CR2
        # return names.apply(lambda x : f"{self.lnik}{'/'.join(x.split['/'])}?idApp=client&dialog=slider&idDialog=%2Fdisk%2F{'%2F'.join(x.split['/'])}")
        return names.apply(self.get_link)

    def h_photo_links(self, names: pd.Series):
        html = []
        for n in self.photo_link(names):
            html.append(f"<a target='_blank' href={n}>{n}</a><br>")
        display(HTML("".join(html)))

    def h_photo_preview(self, names: pd.Series, width=980, height=500):
        html = []
        for n in self.photo_link(names):
            html.append(
                f'<iframe scrolling="no" style="overflow: hidden;"'
                f'src="{n}" width={width} height={height}>{n}</iframe>'
                f'<a target="_blank" href="{n}">></a>'
            )
        display(HTML("".join(html)))  # , width, height))

    def r_rename_file(self, old_name, new_name):
        return run(["rclone", "moveto", f"y:{old_name}", f"y:{new_name}"])

    def a_display_image(self, link, preview_size="preview_size"):
        """display image, link is relative to yandex, preview_size:1024x1024"""
        display(Image(self.a_preview_image(link, preview_size)))

    def a_preview_image(self, link, preview_size):
        meta = self.get_meta(link, fields="preview", preview_size=preview_size)
        return self.get_session().get(meta.preview).content

    def a_return_category(self, link):
        classifier = tf_classifier.default()
        timg = self.a_preview_image(link, "1024x1024")
        im_bytes = np.frombuffer(bytearray(timg), dtype=np.uint8)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        image = cv2.imdecode(im_arr, -1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #plt.imshow(image)
        #plt.show()
        categories = classifier.classify(image.copy())
        return categories
    
