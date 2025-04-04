import json
import os

from tqdm import tqdm

from .dataset import Dataset
from .video import Video


class GOT10kVideo(Video):
    """
    Args:
        name: video name
        root: dataset root
        video_dir: video directory
        init_rect: init rectangle
        img_names: image names
        gt_rect: groundtruth rectangle
        attr: attribute of video
    """

    def __init__(
        self, name, root, video_dir, init_rect, img_names, gt_rect, attr, load_img=False
    ):
        super(GOT10kVideo, self).__init__(
            name, root, video_dir, init_rect, img_names, gt_rect, attr, load_img
        )


class GOT10kDataset(Dataset):
    """
    Args:
        name:  dataset name, should be "NFS30" or "NFS240"
        dataset_root, dataset root dir
    """

    def __init__(self, name, dataset_root, load_img=False):
        super(GOT10kDataset, self).__init__(name, dataset_root)
        with open(os.path.join(dataset_root, name + ".json"), "r") as f:
            meta_data = json.load(f)

        # load videos
        pbar = tqdm(meta_data.keys(), desc="loading " + name, ncols=100)
        self.videos = {}
        for video in pbar:
            pbar.set_postfix_str(video)
            self.videos[video] = GOT10kVideo(
                video,
                dataset_root,
                meta_data[video]["video_dir"],
                meta_data[video]["init_rect"],
                meta_data[video]["img_names"],
                meta_data[video]["gt_rect"],
                None,
            )
        self.attr = {}
        self.attr["ALL"] = list(self.videos.keys())
