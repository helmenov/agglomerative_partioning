#%%
__version__ = "0.1.0"

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def main(ImageFileName, K):
    im = np.array(Image.open(ImageFileName))
    nrows = im.shape[0]
    ncols = im.shape[1]

    feature = im.reshape((nrows * ncols, -1))

    dist = dist_table(feature, nrows, ncols)

    target = agglomerative_clustering(feature, dist, K)

    KclassImage(K, feature, target, (nrows, ncols))


def KclassImage(k, feature, target, shape):

    ktarget = np.copy(target)
    clusterIDs = np.unique(ktarget)
    for i, kk in enumerate(clusterIDs):
        ktarget[np.where(ktarget == kk)[0]] = i

    kfeature = np.copy(feature)
    centroid = np.full(kfeature.shape[1], np.nan)
    for j in range(k):
        centroid = np.mean(kfeature[np.where(ktarget == j)[0], :], axis=0)
        kfeature[np.where(ktarget == j)[0], :] = centroid

    im2 = kfeature.reshape((shape[0], shape[1], -1))
    ImageFileNameK = f"{k}.jpg"
    im2pil = Image.fromarray(im2)
    im2pil.save(ImageFileNameK)
    print(f"\n {k}colored saved")


def dist_table(feature, nrows, ncols):
    print(
        "\nNow Calculating FeatureDistance Table (Geometrical Neighbors only)"
    )
    N_neighbors = 0
    for i in range(len(feature)):
        # Right Pair
        if (i + 1) % ncols != 0:
            N_neighbors += 1
            if N_neighbors == 1:
                entry = np.array(
                    [
                        [
                            i,
                            i + 1,
                            np.sum((feature[i + 1, :] - feature[i, :]) ** 2),
                        ]
                    ]
                )
            else:
                entry = np.concatenate(
                    [
                        entry,
                        [
                            [
                                i,
                                i + 1,
                                np.sum(
                                    (feature[i + 1, :] - feature[i, :]) ** 2
                                ),
                            ]
                        ],
                    ],
                    axis=0,
                )
        # Under Pair
        if (i + ncols) // ncols < nrows:
            N_neighbors += 1
            entry = np.concatenate(
                [
                    entry,
                    [
                        [
                            i,
                            i + ncols,
                            np.sum(
                                (feature[i + ncols, :] - feature[i, :]) ** 2
                            ),
                        ]
                    ],
                ],
                axis=0,
            )
        # Left Under Pair
        if (i + ncols - 1) % ncols != 0 and (i + ncols - 1) // ncols < nrows:
            N_neighbors += 1
            entry = np.concatenate(
                [
                    entry,
                    [
                        [
                            i,
                            i + ncols - 1,
                            np.sum(
                                (feature[i + ncols - 1, :] - feature[i, :])
                                ** 2
                            ),
                        ]
                    ],
                ],
                axis=0,
            )
        # Right Under Pair
        if (i + ncols + 1) % ncols != 0 and (i + ncols + 1) // ncols < nrows:
            N_neighbors += 1
            entry = np.concatenate(
                [
                    entry,
                    [
                        [
                            i,
                            i + ncols + 1,
                            np.sum(
                                (feature[i + ncols + 1, :] - feature[i, :])
                                ** 2
                            ),
                        ]
                    ],
                ],
                axis=0,
            )

        pro_bar = ("=" * int(i / len(feature) * 50)) + (
            " " * int((len(feature) - i) / len(feature) * 50)
        )
        print(
            "\r[{0}] {1:4.2f}%".format(pro_bar, i / len(feature) * 100.0),
            end="",
        )
    return entry


def agglomerative_clustering(feature, dist, K):
    print(f"\nNow Agglomeratively clustering to {K}")
    target = np.array(list(range(len(feature))))
    k0 = len(np.unique(target))
    k = k0
    new_clusterID = k
    while k > K:
        d_nearest = np.amin(dist[:, 2])
        p_nearest = np.where(dist[:, 2] == d_nearest)[0]
        for i, p in enumerate(p_nearest):
            t0 = target[int(dist[p, 0])]
            t1 = target[int(dist[p, 1])]
            if t1 == t0:
                continue
            else:
                new_clusterID += 1
                target[np.where(target == t0)[0]] = new_clusterID
                target[np.where(target == t1)[0]] = new_clusterID
                k = len(np.unique(target))
                pro_bar = (
                    "#" * int(K / k0 * 50)
                    + "=" * int((k - K) / k0 * 50)
                    + "." * int((k0 - k) / k0 * 50)
                )
                print("\r[{0}] Clusters:{1:8d}".format(pro_bar, k), end="")
                # if k in list(map(lambda i: int(i/10*(k0-K)+K), range(1,10))):
                #     print(f'!!{k}!!')
                #     KclassImage(k,feature,target,(1344,760))

                if k <= K:
                    break
        # delete p_nearest lines from dist
        dist = np.delete(dist, obj=p_nearest[: i + 1], axis=0)
    # print(f'Clusters:{k}')

    clusterIDs = np.unique(target)
    for i, k in enumerate(clusterIDs):
        target[np.where(target == k)[0]] = i

    return target


#%%
def agglomerative_clustering2(feature, dist, K):
    """
    distが空になったらkがどうであれ止める
    Args:
        feature ([type]): [description]
        dist ([type]): [description]
        K ([type]): [description]

    Returns:
        [type]: [description]
    """
    print(f"\nNow Agglomeratively clustering to {K}")
    target = np.array(list(range(len(feature))))
    k0 = len(np.unique(target))
    k = k0
    new_clusterID = k

    while k > K:
        d_nearest = np.amin(dist[:, 2])
        p_nearest = np.where(dist[:, 2] == d_nearest)[0]
        for i, p in enumerate(p_nearest):
            t0 = target[int(dist[p, 0])]
            t1 = target[int(dist[p, 1])]
            if t1 == t0:
                continue
            else:
                new_clusterID += 1
                target[np.where(target == t0)[0]] = new_clusterID
                target[np.where(target == t1)[0]] = new_clusterID
                k = len(np.unique(target))
                pro_bar = (
                    "#" * int(K / k0 * 50)
                    + "=" * int((k - K) / k0 * 50)
                    + "." * int((k0 - k) / k0 * 50)
                )
                print("\r[{0}] Clusters:{1:8d}".format(pro_bar, k), end="")
                if k <= K:
                    break
        # delete p_nearest lines from dist
        dist = np.delete(dist, obj=p_nearest[: i + 1], axis=0)
    # print(f'Clusters:{k}')

    clusterIDs = np.unique(target)
    for i, k in enumerate(clusterIDs):
        target[np.where(target == k)[0]] = i

    return target


#%%
if __name__ == "__main__":
    main("sample.jpg", 128)
# %%
